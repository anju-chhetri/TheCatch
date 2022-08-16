from databaseStructure import db, Criminal, Crime, Victim, Judge

#---------------------------------->Kailash
criminalKailash = Criminal(name = "Kailash Pantha", address = "Prem Nagar, Butwal", age = 22, nationality ="Nepali" , years = 5, jail = "Central Jail(Kathmandu)" , fileLocation = "static/image/kailash.jpg" )

crimeKailash = Crime(name ="RDX import", crime_location = "Tribhuvan International Airport",criminal = criminalKailash )

victimKailash = Victim(name = "Asmin Silwal" , address = "Dhadhing", age = 22 , nationality = "Nepali" ,criminal = criminalKailash)

judgeKailash = Judge(name = "Cholendra Shumsher JB Rana", courtName = "Kathmandu District Court" , courtLocation = "Kathmandu" ,casesFought = 55, criminal = criminalKailash)

#--------------------------> Avinash Aryal

criminalAvinash = Criminal(name = "Avinash Aryal", address = "Gulmi", age = 21, nationality ="Nepali" , years = 3, jail = "Kathmandu Jail" , fileLocation = "static/image/avinash.jpg" )

crimeAvinash = Crime(name = "Murder of Prime Minister", crime_location = "Maharajgunj, Kathmandu" ,criminal = criminalAvinash )

victimAvinash = Victim(name = "Sher Bahadur Deuba" , address = "Parliament House" , age = 73, nationality = "Nepali",criminal =criminalAvinash )

judgeAvinash = Judge(name ="Deepak Kumar Karki" , courtName = "Kathmandu High Court", courtLocation = "Babarmahal, Kathmandu" , casesFought = 43, criminal = criminalAvinash )

#------------------>Diwas

criminalDiwas = Criminal(name = "Diwas Ahikari", address = "Patan, Lalitpur", age = 22, nationality ="Nepali" , years = 7, jail = "Nuwakot Jail" , fileLocation = "static/image/diwas.jpg" )

crimeDiwas= Crime(name = "Malware Attack on Chaudhary Group, Nepal", crime_location ="Sanepa, Lalitpur, Nepal" ,criminal = criminalDiwas )

victimDiwas = Victim(name = "Binod Chaudhary" , address = "Kathmandu, Nepal" , age = 70, nationality = "Nepali",criminal = criminalDiwas)

judgeDiwas = Judge(name = "Ishwor Prasad Khatiwada", courtName =  "Kathmandu High Court", courtLocation =  "Babarmahal, Kathmandu", casesFought = 51 , criminal = criminalDiwas)


#-------------------->Pramesh

criminalPramesh= Criminal(name = "Pramesh Shrestha", address = "Lokanthali, Bhaktapur", age = 22, nationality ="Nepali" , years = 9, jail = "Nakhu Jail" , fileLocation = "static/image/pramesh.jpg" )

crimePramesh = Crime(name = "NIC bank Robbery", crime_location = "NIC branch, Lokanthali, Bhaktapus",criminal = criminalPramesh )

victimPramesh = Victim(name = "Tulsi Ram Agrawal", address ="Chitwan, Nepal" , age = 56, nationality = "Nepali",criminal = criminalPramesh )

judgePramesh = Judge(name = "Ananda Mohan Bhattarai", courtName = "Bhaktapur High Court", courtLocation = "Bhaktapus, Nepal", casesFought = 21, criminal = criminalPramesh)


#------------------->Sandesh Sitaula

criminalSandesh = Criminal(name = "Sandesh Sitaula", address = "Jhapa, Nepal", age = 22, nationality ="Nepali" , years = 5, jail = "Jhapa Jail" , fileLocation = "static/image/sandesh.jpg" )
crimeSandesh = Crime(name = "Hostage Taking", crime_location = "Bahundangi, Jhapa, Nepal" ,criminal = criminalSandesh )
victimSandesh = Victim(name = "Prayag Man Mane", address = "Kathmandu, Nepal", age = 21 , nationality = "Nepali",criminal = criminalSandesh)
judgeSandesh = Judge(name = "Sapana Pradhan Malla" , courtName = "Jhapa Hight Court" , courtLocation = "Jhapa, Nepal" , casesFought = 32, criminal = criminalSandesh)

#-------------------->Shiv Narayan Singh

criminalShiv = Criminal(name = "Shiv Narayan Singh", address = "Janakpur, Nepal", age = 23, nationality ="Nepali" , years = 2, jail = "Janakpur Jail" , fileLocation = "static/image/shiv.jpg" )

crimeShiv = Crime(name = "Identity Theft",  crime_location = "Janakpur, Nepal",criminal = criminalShiv )

victimShiv = Victim(name = "Prashant Karn", address = "Kathmandu, Nepal", age = 23 , nationality = "Nepal",criminal = criminalShiv)

judgeShiv = Judge(name = "Hari Krishna Karki", courtName = "Janakpur High Court", courtLocation = "Janakpur, Nepal", casesFought = 19, criminal = criminalShiv )

#-------------------->Trib
criminalTrib = Criminal(name = "Tribhuwan Bhatt", address = "Kathmandu, Nepal", age = 22, nationality ="Nepali" , years = 3, jail = "Gorkha Jail" , fileLocation = "static/image/trib.jpg" )

crimeTrib = Crime(name = "Ransom Money", crime_location = "Gaidakot, Chitwan" ,criminal = criminalTrib  )

victimTrib = Victim(name = "Prabigya Pathak" , address = "Chitwan, Nepal" , age = 23, nationality =  "Nepali",criminal = criminalTrib )

judgeTrib = Judge(name = "Bishowambhar Prasad Shrestha", courtName = "Chitwan High Court", courtLocation = "Birendranagar, Chitwan", casesFought = 23, criminal = criminalTrib)

db.session.add(criminalKailash)
db.session.add_all([crimeKailash, victimKailash, judgeKailash])

db.session.add(criminalAvinash)
db.session.add_all([crimeAvinash, victimAvinash, judgeAvinash])

db.session.add(criminalDiwas)
db.session.add_all([crimeDiwas, victimDiwas, judgeDiwas])

db.session.add(criminalPramesh)
db.session.add_all([crimePramesh, victimPramesh, judgePramesh])

db.session.add(criminalSandesh)
db.session.add_all([crimeSandesh, victimSandesh, judgeSandesh])

db.session.add(criminalShiv)
db.session.add_all([crimeShiv, victimShiv, judgeShiv])

db.session.add(criminalTrib)
db.session.add_all([crimeTrib, victimTrib, judgeTrib])
db.session.commit()



#criminalKailash = Criminal(name = "Kailash Pantha", address = "Prem Nagar, Butwal", age = 22, nationality ="Nepali" , years = 5, jail = "Central Jail(Kathmandu)" , fileLocation = "static/image" )

#crimeKailash = Crime(name =, crime_location = ,criminal =  )

#victimHella = Victim(name = , address = , age = , nationality = ,criminal = )

#judgeHella = Judge(name = , courtName = , courtLocation = , casesFought = , criminal = )
