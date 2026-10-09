import {useEffect,useState,useCallback,lazy,Suspense} from 'react';
import {Orbit,Play,ArrowUpRight,Menu,RotateCcw,SlidersHorizontal,Info,ChevronRight,BookOpen,X} from 'lucide-react';
import Sidebar from './components/Sidebar';
import InfoPanel from './components/InfoPanel';
import Tour from './components/Tour';
import {LEVELS,TOUR_IDS,TOUR_TEXT,validateCatalogue} from './catalogue';
const UniverseCanvas=lazy(()=>import('./components/UniverseCanvas'));
const repo='https://github.com/Fahimxbd/Cosmo200-The-Universe-in-200-Objects';
export default function App(){
 const [data,setData]=useState(null),[error,setError]=useState(''),[level,setLevelState]=useState(2),[selected,setSelected]=useState(null),[info,setInfo]=useState(true),[mobile,setMobile]=useState(false),[low,setLow]=useState(true),[overview,setOverview]=useState(true),[revision,setRevision]=useState(0),[moving,setMoving]=useState(false),[about,setAbout]=useState(false),[allView,setAllView]=useState(false);
 const [tour,setTour]=useState(false),[step,setStep]=useState(0),[playing,setPlaying]=useState(false),[voice,setVoice]=useState(false);
 useEffect(()=>{const c=new AbortController();fetch('/data/objects.json',{signal:c.signal}).then(r=>{if(!r.ok)throw new Error('The catalogue could not be loaded.');return r.json();}).then(d=>{validateCatalogue(d);setData(d);setSelected(d.levels[2].objects[0]);}).catch(e=>{if(e.name!=='AbortError')setError(e.message);});return()=>c.abort();},[]);
 const objects=data?.levels.flatMap(l=>l.objects)||[];
 const stopTour=()=>{setTour(false);setPlaying(false);window.speechSynthesis?.cancel();};
 const select=useCallback(o=>{setAllView(false);setSelected(o);setLevelState(o.level);setInfo(true);setOverview(false);setRevision(r=>r+1);setPlaying(false);},[]);
 function setLevel(i){setAllView(false);setLevelState(i);setSelected(data.levels[i].objects[0]);setOverview(true);setInfo(true);setPlaying(false);setRevision(r=>r+1);}
 function tourStep(i){setAllView(false);setStep(i);const o=objects.find(o=>o.id===TOUR_IDS[i]);setSelected(o);setLevelState(o.level);setOverview(false);setInfo(true);setRevision(r=>r+1);}
 function startTour(){setTour(true);tourStep(0);setPlaying(true);setMobile(false);}
 useEffect(()=>{
  if(!tour||!playing)return;
  let disposed=false,timer;const advance=()=>{if(disposed)return;clearTimeout(timer);if(step<5)tourStep(step+1);else setPlaying(false);};
  if(voice&&'speechSynthesis'in window){const utterance=new SpeechSynthesisUtterance(TOUR_TEXT[step]);utterance.lang='en-US';utterance.rate=.88;utterance.onend=()=>{timer=setTimeout(advance,3500);};utterance.onerror=()=>{timer=setTimeout(advance,16000);};window.speechSynthesis.cancel();window.speechSynthesis.speak(utterance);timer=setTimeout(advance,45000);}else timer=setTimeout(advance,20000);
  return()=>{disposed=true;clearTimeout(timer);window.speechSynthesis?.cancel();};
 },[tour,playing,step,voice,data]);
 useEffect(()=>{const onKey=e=>{if(e.key==='Escape'){setAbout(false);setMobile(false);setInfo(false);stopTour();}};window.addEventListener('keydown',onKey);return()=>window.removeEventListener('keydown',onKey);},[]);
 if(error)return <main className="load-state"><Orbit size={40}/><h1>We couldn't open the atlas.</h1><p>{error}</p><button className="primary-button" onClick={()=>location.reload()}>Try again</button></main>;
 if(!data||!selected)return <main className="load-state"><Orbit className="loading-orbit" size={44}/><h1>Opening the universe</h1><p>Preparing 200 places to explore…</p></main>;
 return <main className="app-shell">
  <header className="topbar"><a className="brand" href="/" aria-label="Cosmo200 home"><span className="brand-mark"><Orbit size={27}/></span><span>cosmo<span className="brand-number">200</span><small>THE UNIVERSE, WITHIN REACH</small></span></a><div className="top-center"><span className="live-dot"/> AN OPEN UNIVERSE FOR EVERYONE</div><div className="top-actions"><a className="github-link" href={repo} target="_blank" rel="noreferrer">Open source <ArrowUpRight size={14}/></a><button className="primary-button" onClick={startTour}><Play size={14} fill="currentColor"/>Take a tour</button></div></header>
  <div className="canvas-wrap"><Suspense fallback={<div className="canvas-fallback">Preparing the 3D canvas…</div>}><UniverseCanvas objects={allView?objects:data.levels[level].objects} allView={allView} selected={selected} level={level} onSelect={select} low={low} overview={overview} revision={revision} onMoving={setMoving}/></Suspense></div>
  <div className="scene-vignette"/>
  <button className="mobile-explore panel" onClick={()=>{setMobile(true);setInfo(false);}}><Menu size={17}/> Explore 200 objects</button>
  {mobile&&<button className="mobile-backdrop" aria-label="Close navigation" onClick={()=>setMobile(false)}/>}
  <Sidebar data={data} objects={objects} level={level} setLevel={setLevel} onSelect={select} selected={selected} open={mobile} onClose={()=>setMobile(false)}/>
  <section className="scene-heading"><div className="eyebrow">YOUR COSMIC PERSPECTIVE <span>0{level+1} / 06</span></div><h1>{allView?'The cosmic atlas':LEVELS[level].name}</h1><p>{LEVELS[level].subtitle}. A little closer to understanding everything.</p><div className="scene-meta"><span className="live-dot"/>{moving?'Travelling through the atlas':`${data.levels[level].count} objects in this collection`}<span className="meta-separator">/</span><span>3D EXPLORER</span></div><button className="all-objects-button" aria-pressed={allView} onClick={()=>{setAllView(!allView);setOverview(true);setRevision(r=>r+1);}}>{allView?'Return to collection':'View all 200 objects'} <ArrowUpRight size={12}/></button></section>
  {info&&!mobile&&<InfoPanel object={selected} onClose={()=>setInfo(false)} onFocus={()=>{setOverview(false);setRevision(r=>r+1);}} onNext={()=>{const list=data.levels[level].objects;select(list[(list.findIndex(o=>o.id===selected.id)+1)%list.length]);}}/>}
  {!info&&!mobile&&<button className="reopen-info panel" onClick={()=>setInfo(true)}><Info size={17}/>{selected.name}<ChevronRight size={15}/></button>}
  {!tour&&<div className="scene-bottom"><span className="eyebrow">A UNIVERSE OF PERSPECTIVE</span><p>Big questions. <em>Wider horizons.</em></p><small>Drag to orbit <span>·</span> Scroll or pinch to zoom <span>·</span> Click to discover</small></div>}
  {tour&&<Tour step={step} playing={playing} voice={voice} setVoice={setVoice} onPlay={()=>setPlaying(!playing)} onStep={tourStep} onClose={stopTour}/>}
  <div className="view-controls panel"><button className="icon-button" title="Reset collection view" aria-label="Reset collection view" onClick={()=>{setOverview(true);setRevision(r=>r+1);}}><RotateCcw size={17}/></button><span/><button className={'icon-button '+(low?'on':'')} title={low?'Eco quality enabled':'High quality enabled'} aria-label="Toggle low-power graphics" aria-pressed={low} onClick={()=>setLow(!low)}><SlidersHorizontal size={17}/></button><span/><button className="icon-button" aria-label="About this educational atlas" onClick={()=>setAbout(true)}><BookOpen size={17}/></button></div>
  <footer className="statusbar"><span><span className="live-dot"/> {low?'ECO RENDERING':'HIGH DETAIL'} <b>·</b> {allView?200:data.levels[level].count} / 200 OBJECTS VISIBLE</span><button onClick={()=>setAbout(true)}>Schematic atlas · not to scale <Info size={11}/></button><span className="scale-label">{LEVELS[level].scale}</span></footer>
  {about&&<div className="modal-scrim" onClick={()=>setAbout(false)}><section className="about-modal panel" role="dialog" aria-modal="true" aria-label="About Cosmo200" onClick={e=>e.stopPropagation()}><button autoFocus className="icon-button modal-close" onClick={()=>setAbout(false)} aria-label="Close about"><X size={20}/></button><Orbit size={34} color="#00d4ff"/><h2>A smaller universe.<br/>A bigger perspective.</h2><p>Cosmo200 is a free, open-source astronomy atlas for schools, colleges, universities, and everyone who looks up.</p><p>All 200 objects are stored locally. The six collections are educational categories, not a physically nested map. Positions, object sizes, colors, and camera transitions are illustrative. The Sun is listed with the Solar System bodies for continuity.</p><p>Images come from NASA's public archive. Some are composites, diagrams, or artist impressions, and some rare objects have no matched image. Always follow the original caption for full context and credit. NASA does not endorse this project.</p><p>Eco mode limits pixel density and geometry. The canvas renders on demand. Narration is optional and depends on browser speech support.</p><a className="primary-button" href={repo} target="_blank" rel="noreferrer">Explore the source <ArrowUpRight size={15}/></a></section></div>}
 </main>;
}
