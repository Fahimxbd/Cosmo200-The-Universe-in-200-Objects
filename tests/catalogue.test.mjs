import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';
import {validateCatalogue,searchObjects,TOUR_IDS} from '../src/catalogue.js';
const data=JSON.parse(fs.readFileSync(new URL('../public/data/objects.json',import.meta.url)));const all=validateCatalogue(data);
test('Exactly 200 unique records in the requested six collections',()=>assert.deepEqual(data.levels.map(l=>l.objects.length),[1,5,20,30,50,94]));
test('Search finds Andromeda by name, alias, and natural prefix',()=>{for(const q of ['Andromeda',' m31 ','Search Andromeda'])assert.equal(searchObjects(all,q)[0].id,8);});
test('Empty and missing searches are safe',()=>{assert.deepEqual(searchObjects(all,''),[]);assert.deepEqual(searchObjects(all,'not-a-real-object'),[]);});
test('Tour visits all six levels in order',()=>assert.deepEqual(TOUR_IDS.map(id=>all.find(o=>o.id===id)?.level),[0,1,2,3,4,5]));
test('Every record includes usable position, description, and distinct identity',()=>{assert.equal(all.length,200);assert.ok(all.every(o=>o.description.length>30&&o.radius>0&&o.position.every(Number.isFinite)));});
