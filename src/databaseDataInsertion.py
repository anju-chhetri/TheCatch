from databaseStructure import db, Criminal, Crime, Victim, Judge

criminal1 = Criminal(name = "Hella", address = "Underworld", age = "400", nationality = "Asgaurdian", years = 200)

crimeHella = Crime(name = "Destruction", crime_location = "Asgaurd", criminal = criminal1 )

victimHella = Victim(name = "Asgaurdians", address = "Asgaurd", age = 100, nationality = "", criminal = criminal1)

judgeHella = Judge(name = "Odin", address = "Asgaurd", age = 1000, country = "Earth", criminal = criminal1)

db.session.add(criminal1)
db.session.add_all([crimeHella, victimHella, judgeHella])
db.session.commit()
