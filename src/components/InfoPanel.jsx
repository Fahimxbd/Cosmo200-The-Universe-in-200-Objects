import {useState,useEffect} from 'react';
import {motion} from 'framer-motion';
import {X,ExternalLink,Focus,ImageOff,ArrowRight} from 'lucide-react';
export default function InfoPanel({object,onClose,onFocus,onNext}){
 const [failed,setFailed]=useState(false);useEffect(()=>setFailed(false),[object.id]);
 return <motion.aside key={object.id} className="info-panel panel" aria-label="Object information" initial={{opacity:0,x:14}} animate={{opacity:1,x:0}} transition={{duration:.25}}>
  <div className="info-top"><span>OBJECT {String(object.id).padStart(3,'0')} / 200</span><button className="icon-button" onClick={onClose} aria-label="Close information"><X size={17}/></button></div>
  <div className="archive-image">{object.image&&!failed?<img loading="lazy" src={object.image.url} alt={object.image.title} onError={()=>setFailed(true)}/>:<div className="image-empty"><ImageOff size={28}/><span>{failed?'Archive image could not load':'No verified NASA image available'}</span></div>}<span className="image-badge">{object.image&&!failed?object.image.kind:'CATALOGUE RECORD'}</span></div>
  <div className="info-content"><span className="eyebrow">{object.type}</span><h2>{object.name}</h2><p className="object-description">{object.description}</p>
  <div className="fact-row"><span>Catalogue ID</span><b>COSMO–{String(object.id).padStart(3,'0')}</b></div>{object.parent&&<div className="fact-row"><span>Orbits / belongs to</span><b>{object.parent}</b></div>}
  <div className="fact-row"><span>Visualization</span><b>Schematic · not to scale</b></div>
  <button className="primary-button focus-button" onClick={onFocus}><Focus size={16}/>Fly to object<ArrowRight size={15}/></button>
  {object.image&&<div className="image-credit"><b>{object.image.title}</b><span>{object.image.credit}</span><a href={object.image.sourceUrl} target="_blank" rel="noreferrer">Original image & full credit <ExternalLink size={11}/></a></div>}
  <a className="text-link" href={object.sourceUrl} target="_blank" rel="noreferrer">Explore NASA science <ExternalLink size={12}/></a><button className="next-object" onClick={onNext}>Next object in collection <ArrowRight size={14}/></button>
  </div>
 </motion.aside>;
}
