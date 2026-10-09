import fs from 'node:fs';
import {validateCatalogue} from '../src/catalogue.js';
const data=JSON.parse(fs.readFileSync(new URL('../public/data/objects.json',import.meta.url)));
const all=validateCatalogue(data);
for(const o of all){if(o.level<0||o.level>5)throw Error('Bad level');if(o.image&&!/^https:\/\/images-assets\.nasa\.gov\//.test(o.image.url))throw Error('Unexpected image host '+o.id);}
console.log(`Validated ${all.length} unique objects; levels: ${data.levels.map(l=>l.count).join(', ')}; NASA archive records: ${all.filter(o=>o.image).length}.`);
