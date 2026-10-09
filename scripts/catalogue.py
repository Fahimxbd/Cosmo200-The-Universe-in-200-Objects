"""Rebuild the curated local catalogue. Run resolve-images.py separately for NASA media."""
import json, math, pathlib
root=pathlib.Path(__file__).resolve().parents[1]
levels=[]
def add(name, label, text):
    rows=[]
    for line in text.strip().splitlines():
        parts=line.split('|'); rows.append(dict(name=parts[0],type=parts[1],description=parts[2],parent=parts[3] if len(parts)>3 else None))
    levels.append(dict(name=name,label=label,count=len(rows),objects=rows))
add('Universe','Universe','''Observable Universe|Universe|The region whose light has had time to reach us. Its present radius is roughly 46 billion light-years; 13.8 billion years is its age, not its radius.''')
add('Superclusters','Supercluster','''Laniakea Supercluster|Supercluster|A region defined by the motions of galaxies, including the Milky Way. Supercluster boundaries depend on how astronomers map them.
Virgo Supercluster|Supercluster|Our local concentration of galaxy groups and clusters, historically called the Local Supercluster.
Coma Supercluster|Supercluster|A large-scale association that includes the rich Coma galaxy cluster.
Shapley Supercluster|Supercluster|A particularly rich concentration of galaxy clusters in the nearby universe.
Perseus-Pisces Supercluster|Supercluster|A long chain of galaxy groups and clusters tracing part of the cosmic web.''')
add('Galaxies','Galaxy','''Milky Way|Barred Spiral Galaxy|Our home galaxy contains at least 100 billion stars. The Solar System lies within its disk.
Andromeda|Spiral Galaxy|Also called M31, this is the nearest large spiral galaxy to the Milky Way and a member of the Local Group.
Triangulum|Spiral Galaxy|M33 is a spiral member of the Local Group, with many regions of active star formation.
Sombrero Galaxy|Galaxy|M104 has a bright central bulge surrounded by a prominent dark dust lane.
Whirlpool Galaxy|Spiral Galaxy|M51 has striking spiral arms shaped by interaction with its companion galaxy.
Pinwheel Galaxy|Spiral Galaxy|M101 is a face-on spiral whose arms contain large regions of star formation.
Black Eye Galaxy|Spiral Galaxy|M64 takes its name from the dark dust band crossing its bright central region.
Large Magellanic Cloud|Dwarf Galaxy|A satellite galaxy of the Milky Way, visible from southern skies.
Small Magellanic Cloud|Dwarf Galaxy|A nearby dwarf galaxy interacting with the Large Magellanic Cloud and the Milky Way.
Elliptical Galaxy M87|Elliptical Galaxy|The giant galaxy whose central black hole was the first imaged by the Event Horizon Telescope.
Centaurus A|Peculiar Galaxy|NGC 5128 has a prominent dust lane and jets powered by its central active black hole.
Cigar Galaxy|Starburst Galaxy|M82 is forming stars intensely and drives a large outflow of gas.
Cartwheel Galaxy|Ring Galaxy|A past encounter generated a ring of star formation, resembling ripples spreading through a disk.
Antennae Galaxies|Merging Galaxies|Two interacting galaxies have long tidal tails and many young star clusters.
Tadpole Galaxy|Disrupted Spiral Galaxy|UGC 10214 has a long tidal tail left by a gravitational encounter.
Hoag's Object|Ring Galaxy|An unusual galaxy with a central body encircled by a ring of young blue stars.
Bode's Galaxy|Spiral Galaxy|M81 is a bright spiral galaxy in the same interacting group as M82.
Centaurus B|Radio Galaxy|PKS 1343-601 is a radio galaxy; radio observations reveal large structures beyond its visible host.
NGC 1300|Barred Spiral Galaxy|A broad central bar connects to sweeping spiral arms.
IC 1101|Elliptical Galaxy|A giant elliptical galaxy at the center of the Abell 2029 galaxy cluster.''')
add('Nebulae & Star Clusters','Nebula','''Orion Nebula|Emission Nebula|M42 is a nearby stellar nursery where young stars illuminate surrounding gas.
Eagle Nebula|Emission Nebula|M16 contains the Pillars of Creation, dense columns of gas and dust shaped by young stars.
Crab Nebula|Supernova Remnant|The expanding debris of the supernova recorded in 1054 contains a rapidly spinning pulsar.
Pleiades|Open Cluster|A nearby cluster of young stars; surrounding dust scatters their blue light.
Carina Nebula|Emission Nebula|A vast star-forming complex containing massive stars and sculpted clouds.
Horsehead Nebula|Dark Nebula|A dense dust cloud seen in silhouette against glowing gas in Orion.
Helix Nebula|Planetary Nebula|The outer layers shed by a dying Sun-like star surround a hot stellar remnant.
Ring Nebula|Planetary Nebula|M57 shows glowing gas expelled during a late stage of stellar evolution.
Dumbbell Nebula|Planetary Nebula|M27 is an expanding cloud of gas surrounding a dying star.
Lagoon Nebula|Emission Nebula|M8 is a stellar nursery containing bright gas, dust lanes, and young stars.
Trifid Nebula|Emission and Reflection Nebula|M20 combines glowing gas, reflected starlight, and dark dust lanes.
Omega Nebula|Emission Nebula|M17 is a bright star-forming region also known as the Swan Nebula.
Rosette Nebula|Emission Nebula|Young stars have cleared a central cavity in a much larger cloud of gas.
Tarantula Nebula|Emission Nebula|30 Doradus is a vigorous star-forming region in the Large Magellanic Cloud.
Cat's Eye Nebula|Planetary Nebula|NGC 6543 has intricate shells formed as a dying star lost material.
Butterfly Nebula|Planetary Nebula|NGC 6302 has two large lobes of gas surrounding a very hot central star.
Boomerang Nebula|Protoplanetary Nebula|A rapidly expanding outflow has made this nebula exceptionally cold.
Veil Nebula|Supernova Remnant|Delicate filaments trace the remains of an exploded star in Cygnus.
Bubble Nebula|Emission Nebula|NGC 7635 contains a bubble blown by the wind of a massive star.
Flame Nebula|Emission Nebula|NGC 2024 is a star-forming cloud crossed by dark lanes of dust.
California Nebula|Emission Nebula|NGC 1499 is an extended glowing cloud in Perseus.
Heart Nebula|Emission Nebula|IC 1805 contains gas ionized by a central group of hot young stars.
Soul Nebula|Emission Nebula|Westerhout 5 is a star-forming complex with cavities and dense pillars.
Pacman Nebula|Emission Nebula|NGC 281 contains young stars and dense globules of gas and dust.
Elephant's Trunk Nebula|Dark Globule|A dense elongated cloud within IC 1396 is shaped by nearby hot stars.
Omega Centauri|Globular Cluster|A massive, dense collection of old stars orbiting the Milky Way.
47 Tucanae|Globular Cluster|A bright southern globular cluster filled with densely packed stars.
Hercules Cluster M13|Globular Cluster|M13 is a prominent northern-sky globular cluster in the Milky Way halo.
Hyades|Open Cluster|A nearby open cluster forms the V-shaped face of Taurus; Aldebaran lies in the foreground.
Beehive Cluster|Open Cluster|M44 is a nearby group of stars in Cancer, visible as a hazy patch under dark skies.''')
add('Star Systems','Star system','''Solar System|Star System|The Sun and its planets, moons, asteroids, comets, and smaller bodies form our planetary system.
Alpha Centauri|Multiple Star System|The nearest stellar system includes Alpha Centauri A, B, and the more distant companion Proxima Centauri.
Sirius|Binary Star|The brightest star in Earth's night sky has a faint white dwarf companion.
Betelgeuse|Red Supergiant|A large evolved star in Orion, nearing the later stages of its life.
Proxima Centauri|Red Dwarf|The closest individual star to the Sun is a member of the Alpha Centauri system.
TRAPPIST-1|Planetary System|An ultracool dwarf star hosts seven known roughly Earth-sized planets.
Kepler-186|Planetary System|This red dwarf hosts Kepler-186f, an Earth-sized planet in its star's habitable zone.
Kepler-452|Planetary System|This Sun-like star hosts the planet candidate commonly discussed as Kepler-452b.
Kepler-22|Planetary System|Kepler-22b orbits this star in the habitable zone; that does not establish that it has life.
Kepler-62|Planetary System|A star with several known planets, including worlds studied for their potential temperate conditions.
Kepler-90|Planetary System|An eight-planet system discovered through transit observations.
Kepler-16|Binary Planetary System|A planet orbits both stars of this binary system.
Kepler-47|Binary Planetary System|A multiple-planet system orbiting a pair of stars.
TOI-700|Planetary System|A red dwarf hosting small planets discovered using TESS observations.
TOI-1452|Planetary System|A red-dwarf system containing a planet investigated as a possible water-rich world.
LHS 1140|Planetary System|A nearby red dwarf hosts planets of interest for atmospheric studies.
LHS 3844|Planetary System|Its close-in rocky planet offers a laboratory for studying airless exoplanets.
L 98-59|Planetary System|A nearby red dwarf with multiple small planets.
GJ 1214|Planetary System|Its sub-Neptune planet is studied to understand cloudy or hazy atmospheres.
Gliese 581|Planetary System|A red dwarf whose planetary signals illustrate the challenges of separating stellar activity from planets.
Gliese 876|Planetary System|A red dwarf with a compact system of gravitationally interacting planets.
Gliese 667|Multiple Star System|A nearby multiple-star system studied in searches for exoplanets.
Gliese 832|Planetary System|A nearby red dwarf with a known giant planetary companion.
Gliese 436|Planetary System|Its Neptune-sized planet has an extended escaping atmosphere.
55 Cancri|Binary Planetary System|A multiple-planet system including the hot super-Earth 55 Cancri e.
51 Pegasi|Planetary System|The first Sun-like star found to host an exoplanet, a close-orbiting gas giant.
HD 209458|Planetary System|Its hot Jupiter helped establish the study of transiting planets and their atmospheres.
HD 189733|Planetary System|A nearby hot-Jupiter system frequently studied by space telescopes.
HD 40307|Planetary System|A star studied for a system of small planets detected through radial velocities.
HD 10180|Planetary System|A Sun-like star with multiple planetary companions.
HD 69830|Planetary System|A star hosting several Neptune-mass planets and circumstellar dust.
HR 8799|Planetary System|Several giant planets have been directly imaged around this young star.
Beta Pictoris|Planetary System|A young star surrounded by a debris disk and directly imaged giant planets.
Vega|Star and Debris Disk|A bright nearby star surrounded by a disk of dusty debris.
Fomalhaut|Multiple Star System|A bright star with a debris ring, part of a wider multiple-star system.
Epsilon Eridani|Planetary System|A nearby young Sun-like star with a planetary companion and debris structures.
Tau Ceti|Star|A nearby Sun-like star studied in planetary searches; proposed small planets remain challenging to confirm.
Barnard's Star|Red Dwarf|A nearby star with a very large apparent motion across the sky.
Wolf 359|Red Dwarf|A faint nearby red dwarf that can produce strong stellar flares.
Lalande 21185|Red Dwarf|One of the nearby red dwarfs studied with precision radial-velocity measurements.
Ross 128|Planetary System|A nearby red dwarf with a small planet in a relatively temperate orbit.
Teegarden's Star|Planetary System|A very cool nearby star with low-mass planetary companions.
K2-18|Planetary System|A red dwarf hosting a sub-Neptune whose atmosphere is studied with spectroscopy; life has not been established.
WASP-12|Planetary System|An extremely hot gas giant orbits close to this star and is losing material.
WASP-39|Planetary System|A gas giant's atmosphere has been studied in detail with the James Webb Space Telescope.
WASP-76|Planetary System|An ultra-hot giant planet demonstrates extreme contrasts between its day and night sides.
WASP-121|Planetary System|A very hot giant planet provides evidence of complex atmospheric chemistry.
PSR B1257+12|Pulsar Planetary System|This pulsar hosts planets, showing that worlds can exist around stellar remnants.
Procyon|Binary Star|A bright nearby star paired with a white dwarf companion.
Capella|Multiple Star System|The bright point in Auriga includes a close pair of giant stars within a wider system.''')
# Solar bodies: preserve supplied IDs 107–116, then add distinct named bodies.
add('Planets & Moons','Planet','''Sun|Star|Our local star powers the Solar System through nuclear fusion in its core.|Solar System
Mercury|Planet|The smallest planet and the closest to the Sun has a heavily cratered surface.|Sun
Venus|Planet|A rocky planet with a dense carbon-dioxide atmosphere and an extreme greenhouse effect.|Sun
Earth|Planet|Our ocean-covered home is the only world currently known to support life.|Sun
Moon|Moon|Earth's natural satellite preserves a long record of impacts on its surface.|Earth
Mars|Planet|A rocky world with polar ice, enormous volcanoes, and evidence of ancient flowing water.|Sun
Jupiter|Gas Giant|The largest planet has powerful storms, a strong magnetic field, and many moons.|Sun
Europa|Moon|Jupiter's icy moon likely hides a global ocean beneath its crust.|Jupiter
Saturn|Gas Giant|A gas giant surrounded by rings made mainly of countless pieces of water ice.|Sun
Titan|Moon|Saturn's largest moon has a thick atmosphere and lakes of liquid methane and ethane.|Saturn
Uranus|Ice Giant|This ice giant rotates on its side relative to its orbit.|Sun
Neptune|Ice Giant|The outermost major planet has a dynamic atmosphere and powerful winds.|Sun
Pluto|Dwarf Planet|A Kuiper Belt dwarf planet with mountains of water ice and plains of nitrogen ice.|Sun
Ceres|Dwarf Planet|The largest object in the main asteroid belt contains salts and evidence of past brines.|Sun
Eris|Dwarf Planet|A distant icy dwarf planet with a moon named Dysnomia.|Sun
Haumea|Dwarf Planet|A rapidly rotating, elongated dwarf planet with a ring and two known moons.|Sun
Makemake|Dwarf Planet|A cold dwarf planet in the Kuiper Belt with a known small moon.|Sun
Phobos|Moon|The larger Martian moon is irregularly shaped and orbits close to Mars.|Mars
Deimos|Moon|The smaller Martian moon has a dusty, cratered surface.|Mars
Io|Moon|Tidal heating makes this Jovian moon intensely volcanically active.|Jupiter
Ganymede|Moon|The largest moon in the Solar System has its own magnetic field.|Jupiter
Callisto|Moon|An ancient, heavily cratered Jovian moon with evidence suggesting a subsurface ocean.|Jupiter
Enceladus|Moon|Jets from its south polar region carry water ice from a subsurface ocean into space.|Saturn
Mimas|Moon|A small icy Saturnian moon dominated visually by its large Herschel crater.|Saturn
Tethys|Moon|An icy moon of Saturn with a huge crater and a long canyon system.|Saturn
Dione|Moon|An icy Saturnian moon with bright fractures and a heavily cratered surface.|Saturn
Rhea|Moon|Saturn's second-largest moon is icy and densely cratered.|Saturn
Iapetus|Moon|One hemisphere is much darker than the other, and a ridge follows part of its equator.|Saturn
Hyperion|Moon|A porous, irregular Saturnian moon with chaotic rotation and a sponge-like appearance.|Saturn
Phoebe|Moon|An outer irregular moon of Saturn on a retrograde orbit, probably captured long ago.|Saturn
Miranda|Moon|Uranus's small moon has a dramatically varied landscape of cliffs and ridges.|Uranus
Ariel|Moon|A Uranian moon with bright icy terrain cut by valleys and faults.|Uranus
Umbriel|Moon|A dark Uranian moon whose surface is heavily cratered.|Uranus
Titania|Moon|Uranus's largest moon has impact craters and large fault valleys.|Uranus
Oberon|Moon|A large outer moon of Uranus with an old, cratered surface.|Uranus
Triton|Moon|Neptune's largest moon orbits retrograde and is thought to be a captured Kuiper Belt object.|Neptune
Nereid|Moon|An outer Neptunian moon following a strongly elongated orbit.|Neptune
Proteus|Moon|A dark, irregular moon of Neptune imaged during Voyager 2's flyby.|Neptune
Charon|Moon|Pluto's largest moon is large enough that the pair orbit a point outside Pluto.|Pluto
Nix|Moon|A small irregular moon in the Pluto system visited by New Horizons.|Pluto
Hydra|Moon|An outer small moon of Pluto with a reflective icy surface.|Pluto
Kerberos|Moon|A small, irregularly shaped member of Pluto's satellite system.|Pluto
Styx|Moon|A small moon orbiting between Charon and Nix in the Pluto system.|Pluto
Dysnomia|Moon|Eris's known moon helps astronomers measure the dwarf planet's mass.|Eris
Hi'iaka|Moon|The larger of Haumea's two known moons has a water-ice-rich surface.|Haumea
Namaka|Moon|The smaller of Haumea's known moons follows a tilted orbit.|Haumea''')
moons={
'Jupiter':'Amalthea,Thebe,Adrastea,Metis,Himalia,Elara,Pasiphae,Sinope,Lysithea,Carme,Ananke,Leda,Callirrhoe,Themisto,Megaclite,Taygete,Chaldene,Harpalyke,Kalyke,Iocaste,Erinome',
'Saturn':'Janus,Epimetheus,Atlas,Prometheus,Pandora,Pan,Daphnis,Telesto,Calypso,Helene,Polydeuces,Paaliaq,Siarnaq,Tarvos,Ijiraq',
'Uranus':'Puck,Portia,Juliet,Cressida,Desdemona,Rosalind,Belinda,Cordelia,Ophelia',
'Neptune':'Larissa,Galatea,Despina'}
for parent,names in moons.items():
    for name in names.split(','):
        desc=f'{name} is a natural satellite of {parent}. Comparing satellite orbits helps astronomers investigate the formation and evolution of planetary systems.'
        levels[-1]['objects'].append(dict(name=name,type='Moon',description=desc,parent=parent))
levels[-1]['count']=len(levels[-1]['objects'])
assert [l['count'] for l in levels]==[1,5,20,30,50,94], [l['count'] for l in levels]
idx=0
for li,l in enumerate(levels):
    for j,o in enumerate(l['objects']):
        idx+=1; o['id']=idx; o['level']=li
        # Positions are an atlas layout, never astronomical coordinates.
        angle=j*2.3999632297; radius=0 if j==0 else 14+math.sqrt(j)*10
        o['position']=[round(math.cos(angle)*radius,3),round(math.sin(j*1.7)*radius*.22,3),round(math.sin(angle)*radius,3)]
        o['radius']=[16,6,16 if j==0 else 4,3,2,1.8][li]*(1 if j==0 else .6+.35*((j*7)%9)/9)
        o['color']=['#96ceff','#86abff','#b8caff','#dca6ff','#ffe0aa','#78c6ee'][li]
        o['nasaQuery']=o['name'].replace('Elliptical Galaxy ','').replace('Hercules Cluster ','')
        o['image']=None
        o['sourceUrl']='https://science.nasa.gov/solar-system/' if li==5 else 'https://science.nasa.gov/universe/'
        o['aliases']={'Andromeda':['M31','NGC 224'],'Milky Way':['Our galaxy'],'Moon':['Luna'],'Whirlpool Galaxy':['M51'],'Orion Nebula':['M42'],'Pleiades':['M45'],'Solar System':['Sol'],'Sun':['Sol star']}.get(o['name'],[])
(root/'public/data/objects.json').write_text(json.dumps({'schemaVersion':1,'layoutNotice':'Schematic educational atlas. Positions, sizes, and transitions are not to physical scale. Levels are categories, not a universal containment tree.','levels':levels},ensure_ascii=False,indent=2)+'\n')
print('Generated',idx,'objects')
