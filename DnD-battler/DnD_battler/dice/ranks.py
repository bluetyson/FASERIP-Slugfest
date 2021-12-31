import random

dict_faserip={"Sh0":0,"Fb":2,"Pr":4,"Ty":6,"Gd":10,"Ex":20,"Rm":30,"In":40,"Am":50,"Mn":75,"Un":100,"ShX":150,"ShY":200,"ShZ":500,"Cl1000":1000,"Cl3000":3000,"Cl5000":5000,"Beyond":1000000000}

faserip_index={"Sh0":0,"Fb":1,"Pr":2,"Ty":3,"Gd":4,"Ex":5,"Rm":6,"In":7,"Am":8,"Mn":9,"Un":10,"ShX":11,"ShY":12,"ShZ":13,"Cl1000":14,"Cl3000":15,"Cl5000":16,"Beyond":17}

Sh0 = {"W":-1, "G":66, "Y":95, "R":100}
Fb = {"W":-1, "G":61, "Y":91, "R":100}
Pr = {"W":-1, "G":56, "Y":86, "R":100}
Ty = {"W":-1, "G":51, "Y":81, "R":98}
Gd = {"W":-1, "G":46, "Y":76, "R":98}
Ex = {"W":-1, "G":41, "Y":71, "R":95}
Rm = {"W":-1, "G":36, "Y":66, "R":95}
In = {"W":-1, "G":31, "Y":61, "R":91}
Am = {"W":-1, "G":26, "Y":56, "R":91}
Mn = {"W":-1, "G":21, "Y":51, "R":86}
Un = {"W":-1, "G":16, "Y":46, "R":86}
ShX = {"W":-1, "G":11, "Y":41, "R":81}
ShY = {"W":-1, "G":7, "Y":41, "R":81}
ShZ = {"W":-1, "G":4, "Y":36, "R":76}
Cl1000 = {"W":-1, "G":2, "Y":36, "R":76}
Cl3000 = {"W":-1, "G":2, "Y":31, "R":71}
Cl5000 = {"W":-1, "G":2, "Y":26, "R":66}
Beyond = {"W":-1, "G":2, "Y":21, "R":61}

universal_table_list = [Sh0,Fb,Pr,Ty,Gd,Ex,Rm,In,Am,Mn,Un,ShX,ShY,ShZ,Cl1000,Cl3000,Cl5000,Beyond]
universal_table = {"Sh0":0,"Fb":2,"Pr":4,"Ty":6,"Gd":10,"Ex":20,"Rm":30,"In":40,"Am":50,"Mn":75,"Un":100,"ShX":150,"ShY":200,"ShZ":500,"Cl1000":1000,"Cl3000":3000,"Cl5000":5000,"Beyond":1000000000}

for index, key in enumerate(universal_table.keys()):
	universal_table[key] = universal_table_list[index]

def universal_color(rank, roll):
	if roll >= universal_table[rank]['R']:
		color = 'R'
	elif roll >= universal_table[rank]['Y']:
		color = 'Y'
	elif roll >= universal_table[rank]['G']:		
		color = 'G'
	else:
		color = 'W'
	return color

def column_shift(rank, shift):
	rank_list = []
	for key in faserip_index.keys():
		rank_list.append(key)
	rank_index = faserip_index[rank]
	new_index = rank_index + shift
	if new_index < 0: #lowest is zero
		new_index = 0
	if new_index > 13: #keep under cosmic
		new_index = 13
		
	return rank_list[new_index] #give back adjusted rank

	
def slam_check(endurance_rank):
	endurance_roll = random.randint(1,100)
	color = universal_color(endurance_rank, endurance_roll)
	if color == "W":
		result = "Grand Slam"
	if color == "G":
		result = "Slam"
	if color == "Y":
		result = "Stagger"
	if color == "R":
		result = "No"
	return result
	
def stun_check(endurance_rank):
	endurance_roll = random.randint(1,100)
	color = universal_color(endurance_rank, endurance_roll)
	if color == "W":
		result = random.randint(1,10)
	if color == "G":
		result = 1
	if color == "Y":
		result = 0
	if color == "R":
		result = 0
	return result
	
def kill_check(endurance_rank):
	endurance_roll = random.randint(1,100)
	color = universal_color(endurance_rank, endurance_roll)
	if color == "W":
		result = "En Loss"
	if color == "G":
		result = "E S"
	if color == "Y":
		result = "No"
	if color == "R":
		result = "No"
	return result
