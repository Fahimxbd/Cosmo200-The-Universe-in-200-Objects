import {useState,useMemo} from 'react';
import {Search,ArrowUpRight,ChevronRight,X} from 'lucide-react';
import {LEVELS,searchObjects} from '../catalogue';
export default function Sidebar({data,objects,level,setLevel,onSelect,selected,open,onClose}){
 const [query,setQuery]=useState('');const matches=useMemo(()=>searchObjects(objects,query),[objects,query]);const choose=o=>{onSelect(o);setQuery('');onClose();};
 return <aside className={'sidebar panel '+(open?'mobile-open':'')} aria-label="Universe explorer">
  <div className="mobile-sidebar-heading"><b>Explore the atlas</b><button className="icon-button" aria-label="Close explorer" onClick={onClose}><X size={18}/></button></div>
  <form className="search-box" role="search" onSubmit={e=>{e.preventDefault();if(matches[0])choose(matches[0]);}}><Search size={17}/><input aria-label="Search 200 objects" value={query} onChange={e=>setQuery(e.target.value)} placeholder="Search the universe…"/><kbd>↵</kbd></form>
  {query.trim()&&<div className="search-results" aria-live="polite">{matches.length?matches.map(o=><button key={o.id} onClick={()=>choose(o)}><span>{o.name}<small>{o.type}</small></span><ArrowUpRight size={15}/></button>):<p>No objects found. Try “Andromeda” or “M31”.</p>}</div>}
  <div className="section-label">SCALE OF THE UNIVERSE <span>06</span></div>
  <nav className="level-list" aria-label="Six zoom levels">{LEVELS.map((l,i)=><button key={l.name} className={'level-button '+(i===level?'active':'')} aria-pressed={i===level} onClick={()=>{setLevel(i);onClose();}}><span className="level-symbol">{l.icon}</span><span className="level-copy">{l.name}<small>{l.subtitle}</small></span><span className="level-count">{data.levels[i].count}</span>{i===level&&<ChevronRight size={14}/>}</button>)}</nav>
  <div className="sidebar-divider"/>
  <div className="section-label">IN THIS COLLECTION <span>{data.levels[level].count}</span></div>
  <div className="catalogue-list">{data.levels[level].objects.map(o=><button className={selected.id===o.id?'current':''} key={o.id} onClick={()=>choose(o)}><span className="tiny-dot" style={{background:o.color}}/><span>{o.name}</span><ArrowUpRight size={13}/></button>)}</div>
  <div className="sidebar-foot"><span className="live-dot"/>200 objects. Infinite curiosity.<small>Free for every curious mind.</small></div>
 </aside>;
}
