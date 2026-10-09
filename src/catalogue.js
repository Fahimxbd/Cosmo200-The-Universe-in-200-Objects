export const LEVELS = [
 {name:'Universe',subtitle:'The cosmic horizon',scale:'Billions of light-years',color:'#a9cfff',icon:'◎'},
 {name:'Superclusters',subtitle:'The cosmic web',scale:'Hundreds of millions of light-years',color:'#86abff',icon:'✧'},
 {name:'Galaxies',subtitle:'Islands of stars',scale:'Thousands of light-years',color:'#00d4ff',icon:'◉'},
 {name:'Nebulae & clusters',subtitle:'Where stars are born',scale:'Tens of light-years',color:'#dca6ff',icon:'✦'},
 {name:'Star systems',subtitle:'Stellar neighborhoods',scale:'Light-years to astronomical units',color:'#ffe0aa',icon:'☼'},
 {name:'Planets & moons',subtitle:'Worlds to discover',scale:'Thousands of kilometers',color:'#78c6ee',icon:'◒'},
];
export const TOUR_IDS=[1,2,7,27,57,110];
export const TOUR_TEXT=[
 'Begin with the observable universe. Its light has had time to reach us. Expansion means its present radius is about 46 billion light-years, although the universe is about 13.8 billion years old.',
 'Zoom into the cosmic web. Galaxies gather into groups, clusters, and larger structures. Laniakea is defined using galaxy motions, and includes our cosmic neighborhood.',
 'Meet the Milky Way, our home galaxy. At least 100 billion stars belong to this vast barred spiral. The Sun is one of them, far from the central bulge.',
 'Explore the Orion Nebula, a stellar nursery. Gravity gathers gas and dust into new stars. Not all nebulae form stars: some are the remains of dying stars.',
 'Enter the Solar System. The Sun holds planets, moons, asteroids, and comets in orbit. Other stars have planetary systems too, and their arrangements can be very different.',
 'Arrive at Earth, our ocean world. It is the only planet known to support life. This atlas compresses distances and sizes so we can explore these very different scales together.',
];
export function searchObjects(objects,query){const q=query.trim().toLowerCase().replace(/^search\s+/,'');if(!q)return [];return objects.filter(o=>[o.name,o.type,...o.aliases].some(s=>s.toLowerCase().includes(q))).sort((a,b)=>Number(b.name.toLowerCase()===q)-Number(a.name.toLowerCase()===q)).slice(0,12);}
export function validateCatalogue(data){
 const expected=[1,5,20,30,50,94];if(data.levels?.length!==6)throw new Error('Expected six levels.');
 const all=data.levels.flatMap((l,i)=>{if(l.count!==expected[i]||l.objects.length!==expected[i])throw new Error('Incorrect level count.');return l.objects;});
 if(new Set(all.map(o=>o.id)).size!==200||new Set(all.map(o=>o.name)).size!==200)throw new Error('Catalogue must contain 200 unique objects.');
 all.forEach((o,i)=>{if(o.id!==i+1||!o.description||!o.name||!o.type||!Array.isArray(o.position)||o.position.length!==3||!o.position.every(Number.isFinite))throw new Error('Invalid object '+o.id);});return all;
}
