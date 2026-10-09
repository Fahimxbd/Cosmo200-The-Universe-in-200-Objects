import React,{useMemo,useRef,useEffect,Component} from 'react';
import {Canvas,useFrame,useThree} from '@react-three/fiber';
import {OrbitControls,Html,Detailed} from '@react-three/drei';
import * as THREE from 'three';
function random(seed){return ()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;};}
function dustGeometry(kind,count){
 const rand=random(812+kind),p=new Float32Array(count*3),c=new Float32Array(count*3);
 for(let i=0;i<count;i++){
  const r=Math.pow(rand(),.65)*4.7,a=rand()*Math.PI*2,arm=(i%3)*Math.PI*2/3;
  const angle=kind===2?arm+r*.95+(rand()-.5)*.55:a;
  p[i*3]=Math.cos(angle)*r;p[i*3+1]=(rand()-.5)*(kind===2?.5:4);p[i*3+2]=Math.sin(angle)*r;
  const col=new THREE.Color().setHSL(kind===3?.77: .59-r*.018,.35, .55+rand()*.4);c.set(col.toArray(),i*3);
 }const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.BufferAttribute(p,3));g.setAttribute('color',new THREE.BufferAttribute(c,3));return g;
}
function Backdrop(){
 const geometry=useMemo(()=>{const rand=random(42),p=new Float32Array(900*3);for(let i=0;i<900;i++){const theta=rand()*Math.PI*2,z=rand()*2-1,r=650;const s=Math.sqrt(1-z*z);p.set([r*s*Math.cos(theta),r*z,r*s*Math.sin(theta)],i*3);}const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.BufferAttribute(p,3));return g;},[]);
 useEffect(()=>()=>geometry.dispose(),[geometry]);return <points geometry={geometry}><pointsMaterial color="#aec2dd" size={.8} transparent opacity={.6} sizeAttenuation /></points>;
}
function CosmicObject({object,selected,onSelect,geometry,low,labels}){
 const o=object;const gas=o.level<=3;const pick=e=>{e.stopPropagation();onSelect(o);};
 return <group position={o.position}>
  <group rotation={o.level===2?[.2,0,-.23]:[0,0,0]}>
   <Detailed distances={[0,selected?1000:(low?75:160)]} hysteresis={.12}>
    <group>
     {gas&&<points geometry={geometry} scale={o.radius/2.4}><pointsMaterial size={low?.3:.25} vertexColors transparent opacity={.92} depthWrite={false} blending={THREE.AdditiveBlending}/></points>}
     <mesh scale={gas?[1,.55,1]:[1,1,1]} onClick={pick}><sphereGeometry args={[gas?o.radius*.23:o.radius,24,16]}/><meshStandardMaterial color={o.color} emissive={o.color} emissiveIntensity={gas?.9:.23} roughness={.8}/></mesh>
     {o.name==='Saturn'&&<mesh rotation={[-Math.PI/2+.3,0,0]}><ringGeometry args={[o.radius*1.3,o.radius*2,48]}/><meshBasicMaterial color="#c6b08c" side={THREE.DoubleSide} transparent opacity={.75}/></mesh>}
     {o.name==='Earth'&&<mesh rotation={[.4,0,.4]}><icosahedronGeometry args={[o.radius*1.008,1]}/><meshBasicMaterial color="#82cc9f" wireframe transparent opacity={.7}/></mesh>}
    </group>
    <mesh onClick={pick}><icosahedronGeometry args={[gas?o.radius*.8:o.radius,0]}/><meshBasicMaterial color={o.color}/></mesh>
   </Detailed>
  </group>
  {/* Invisible hit target remains generous even at low detail. */}
  <mesh onClick={pick}><sphereGeometry args={[o.radius*1.5,8,6]}/><meshBasicMaterial transparent opacity={0} depthWrite={false}/></mesh>
  {selected&&<mesh rotation={[-Math.PI/2,0,0]}><ringGeometry args={[o.radius*2.4,o.radius*2.43,64]}/><meshBasicMaterial color="#00d4ff" transparent opacity={.5} side={THREE.DoubleSide}/></mesh>}
  {(selected||labels)&&<Html position={[0,o.radius*1.8,0]} center zIndexRange={[5,0]}><button tabIndex={-1} onClick={()=>onSelect(o)} className={'object-label '+(selected?'selected':'')}>{o.name}{selected&&<span>SELECTED OBJECT</span>}</button></Html>}
 </group>;
}
function CameraRig({focus,level,overview,revision,onMoving,allView}){
 const controls=useRef(),flight=useRef(null),{camera,invalidate}=useThree();
 useEffect(()=>{
  const endTarget=new THREE.Vector3(...(overview?[0,0,0]:focus.position));
  const distance=overview?(allView?840:[65,115,175,200,260,330][level]):Math.max(18,focus.radius*(level<=3?10:7));
  const endPosition=endTarget.clone().add(new THREE.Vector3(distance*.2,distance*.4,distance));
  flight.current={time:0,startPosition:camera.position.clone(),startTarget:controls.current?.target.clone()||new THREE.Vector3(),endPosition,endTarget};
  onMoving(true);invalidate();
 },[focus.id,level,overview,revision]);
 useFrame((_,dt)=>{
  if(!flight.current||!controls.current)return;const f=flight.current;f.time+=Math.min(dt,.05);const t=Math.min(f.time/(window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 0.1 : 1.8),1),ease=t*t*(3-2*t);
  camera.position.lerpVectors(f.startPosition,f.endPosition,ease);controls.current.target.lerpVectors(f.startTarget,f.endTarget,ease);controls.current.update();
  if(t<1)invalidate();else{flight.current=null;onMoving(false);}
 });
 return <OrbitControls ref={controls} makeDefault enableDamping dampingFactor={.12} minDistance={3} maxDistance={900} enablePan onStart={()=>{flight.current=null;onMoving(false);}}/>;
}
class CanvasBoundary extends Component{state={error:false};static getDerivedStateFromError(){return {error:true};}render(){return this.state.error?<div className="canvas-fallback"><h2>Explore in catalogue mode</h2><p>3D is unavailable on this device. Search and browse all 200 objects using the sidebar.</p></div>:this.props.children;}}
export default function UniverseCanvas({objects,selected,level,onSelect,low,overview,revision,onMoving,allView}){
 const geometry=useMemo(()=>dustGeometry(level,low?1000:2000),[level,low]);useEffect(()=>()=>geometry.dispose(),[geometry]);
 return <CanvasBoundary><Canvas aria-label="Interactive schematic universe. Use search or the object list for keyboard navigation." frameloop="demand" dpr={low?1:[1,1.5]} camera={{position:[30,65,210],fov:48,near:.1,far:1800}} gl={{antialias:!low,powerPreference:'low-power'}} fallback={<div className="canvas-fallback">3D is not supported. Use the searchable catalogue to explore.</div>}>
  <color attach="background" args={['#000000']}/><ambientLight intensity={1.5}/><directionalLight position={[10,20,15]} intensity={2}/><Backdrop/>
  <group>{objects.map((o,i)=><CosmicObject key={o.id} object={allView?{...o,position:[o.position[0]+Math.cos(o.level*Math.PI/3)*210,o.position[1],o.position[2]+Math.sin(o.level*Math.PI/3)*210]}:o} selected={selected.id===o.id} onSelect={()=>onSelect(o)} geometry={geometry} low={low} labels={i<4&&overview}/>)}</group>
  <gridHelper args={[300,24,'#123244','#08151d']} position={[0,-22,0]} material-transparent material-opacity={.22}/>
  <CameraRig focus={selected} level={level} overview={overview} revision={revision} onMoving={onMoving} allView={allView}/>
 </Canvas></CanvasBoundary>;
}
