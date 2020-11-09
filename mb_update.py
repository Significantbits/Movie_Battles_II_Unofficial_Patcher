from urllib import request
from random import choice
import requests
import sys
import os
import html5lib

user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
        ' Edge/17.17134',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'
]

title = ".___  ___.   ______   ____    ____  __   _______    .______        ___   .___________.___________. __       _______     _______.    __   __\n|   \/   |  /  __  \  \   \  /   / |  | |   ____|   |   _  \      /   \  |           |           ||  |     |   ____|   /       |   |  | |  |\n|  \  /  | |  |  |  |  \   \/   /  |  | |  |__      |  |_)  |    /  ^  \ `---|  |----`---|  |----`|  |     |  |__     |   (----`   |  | |  |\n|  |\/|  | |  |  |  |   \      /   |  | |   __|     |   _  <    /  /_\  \    |  |        |  |     |  |     |   __|     \   \       |  | |  |\n|  |  |  | |  `--'  |    \    /    |  | |  |____    |  |_)  |  /  _____  \   |  |        |  |     |  `----.|  |____.----)   |      |  | |  |\n|__|  |__|  \______/      \__/     |__| |_______|   |______/  /__/     \__\  |__|        |__|     |_______||_______|_______/       |__| |__| "


name = " __    __  .__   __.   ______    _______  _______  __    ______  __       ___       __         .______      ___   .___________.  ______  __    __   _______ .______      \n|  |  |  | |  \ |  |  /  __  \  |   ____||   ____||  |  /      ||  |     /   \     |  |        |   _  \    /   \  |           | /      ||  |  |  | |   ____||   _  \     \n|  |  |  | |   \|  | |  |  |  | |  |__   |  |__   |  | |  ,----'|  |    /  ^  \    |  |        |  |_)  |  /  ^  \ `---|  |----`|  ,----'|  |__|  | |  |__   |  |_)  |    \n|  |  |  | |  . `  | |  |  |  | |   __|  |   __|  |  | |  |     |  |   /  /_\  \   |  |        |   ___/  /  /_\  \    |  |     |  |     |   __   | |   __|  |      /     \n|  `--'  | |  |\   | |  `--'  | |  |     |  |     |  | |  `----.|  |  /  _____  \  |  `----.   |  |     /  _____  \   |  |     |  `----.|  |  |  | |  |____ |  |\  \----.\n \______/  |__| \__|  \______/  |__|     |__|     |__|  \______||__| /__/     \__\ |_______|   | _|    /__/     \__\  |__|      \______||__|  |__| |_______|| _| `._____|"



def save_response_content(response,destination):
	CHUNK_SIZE = 32768

	with open(destination,'wb') as f:
		for chunk in response.iter_content(CHUNK_SIZE):
			if chunk:
				f.write(chunk)

def get_confirm_token(response):
	for key,value in response.cookies.items():
		if key.startswith('download_warning'):
			return value

	return None


def download_file_from_google_drive(url,id,destination):
	session = requests.Session()

	response = session.get(url, params = {'id' : id}, stream = True)
	token = get_confirm_token(response)

	if token:
		params = {'id' : id,'confirm' : token}
		response = session.get(url, params = params,stream = True)
	save_response_content(response,destination)

def update_seasonal(game_data_dir,doc):
	# Check seasonal
	temp = doc.xpath('//b/text()')
	links = []
	if 'Seasonal Patch' in temp:
		print("Checking Seasonal Patch...")
		temp = doc.xpath('//a/@href')
		for t in temp:
			if "drive.google" in t:
				links += [t]
	
		seasonal_url = links[2]
		file_id = seasonal_url.split("/view")
		seasonal_url = file_id[0]
		file_id = seasonal_url.split("/")[-1]
		seasonal_url = "https://drive.google.com/u/0/uc?id=" + file_id + "&export=download"

		req = request.Request(seasonal_url, headers={
						'User-Agent' : choice(user_agents),
		})
		r = request.urlopen(req)
		t_doc = html5lib.parse(r, treebuilder='lxml',namespaceHTMLElements=False)
		seasonal_version = t_doc.xpath('//span[@class="uc-name-size"]/a/text()')[0]
		try:
			sf = open(game_data_dir + "/seasonal_patch.txt","r")
			if sf.readline() == seasonal_version:
				print("Seasonal Patch already installed!")
				return
		except FileNotFoundError:
			print("")
			
		print("Downloading seasonal patch...")
		os.system("mkdir temp_patch")
		download_file_from_google_drive(seasonal_url,file_id, "./temp_patch/patch.zip")
		print("Unpacking seasonal patch...")
		os.system("cd temp_patch ; unzip patch.zip ; cd ../")
		patch_files = os.listdir("./temp_patch")
		for f in patch_files:
			if ".dll" in f or ".bat" in f:
				continue

			if f == "MBII":
				MBII_files = os.listdir("./temp_patch/MBII")
				for mb_f in MBII_files:
					os.system("cd ./temp_patch/MBII ; cp " + mb_f.replace(" ","\ ") + " " + game_data_dir.replace(" ","\ ") + "MBII/" + " ; cd ../../")
			else:
				os.system("cd ./temp_patch ; cp " + f.replace(" ","\ ") + " " + game_data_dir.replace(" ","\ ") + " ; cd ../")




		sf = open(game_data_dir + "/seasonal_patch.txt","w")
		sf.write(seasonal_version)
		sf.close()
		os.system("rm -rf temp_patch")

def update_game(game_data_dir,version):
	# Check game
	f = open(game_data_dir + "MBII/" + "version.info","r")
	local_version = f.readline()
	f.close()
	
	if not (local_version == version):
		# Update
		temp = doc.xpath('//a/@href')
		links = []
		for t in temp:
			if "drive.google" in t:
				links += [t]

		update_link = links[1]
		file_id = update_link.split("/view")
		update_link = file_id[0]
		file_id = update_link.split("/")[-1]
		update_link = "https://drive.google.com/u/0/uc?id=" + file_id + "&export=download"

		print("Downloading patch...")
		os.system("mkdir temp_patch")
		download_file_from_google_drive(update_link,file_id, "./temp_patch/patch.zip")
		print("Unpacking patch...")
		os.system("cd temp_patch ; unzip patch.zip ; cd ../")
		patch_files = os.listdir("./temp_patch")
		for f in patch_files:
			if ".dll" in f or ".bat" in f:
				continue

			if f == "MBII":
				MBII_files = os.listdir("./temp_patch/MBII")
				for mb_f in MBII_files:
					os.system("cd ./temp_patch/MBII ; cp " + mb_f.replace(" ","\ ") + " " + game_data_dir.replace(" ","\ ") + "MBII/" + " ; cd ../../")
			else:
				os.system("cd ./temp_patch ; cp " + f.replace(" ","\ ") + " " + game_data_dir.replace(" ","\ ") + " ; cd ../")

		vf = open(game_data_dir + "/MBII" + "/version.info","w")
		vf.write(version)
		vf.close()
		os.system("rm -rf temp_patch")


def update(game_data_dir,version,doc):
	try:
		f = open(game_data_dir + "MBII/" + "version.info","r")
		f.close()
	except FileNotFoundError:
		print("This doesn't look like the Game Data directory. Exiting...")
		print("Usage:\n" + usage)
		quit()


	# Check game
	update_game(game_data_dir,version)

	# Check seasonal
	update_seasonal(game_data_dir,doc)
	print("Movie Battles II is up to date! Have fun!")

def install_mb(game_data_dir,doc):
	# Install Open JK
	try:
		f = open(game_data_dir + "version.inf","r")
		f.close()
	except FileNotFoundError:
		print("This doesn't look like the Game Data directory. Exiting...")
		print("Usage:\n" + usage)
		quit()

	os.system("mkdir temp_openjk")
	print("Downloading OpenJK...")
	response = requests.get("https://builds.openjk.org/openjk-2018-02-26-e3f22070-linux.tar.gz")
	with open("./temp_openjk/openjk-2018-02-26-e3f22070-linux.tar.gz","wb") as f:
		f.write(response.content)
	print("Unpacking OpenJK...")
	os.system("cd temp_openjk ;  tar -xvf openjk-2018-02-26-e3f22070-linux.tar.gz ; cd ../")
	print("Installing OpenJK...")
	open_jk_files = os.listdir("./temp_openjk/install/JediAcademy/")
	for jk_f in open_jk_files:
		if jk_f == "openjk-2018-02-26-e3f22070-linux.tar.gz":
			continue
		if jk_f == "base":
			base_files = os.listdir("./temp_openjk/install/JediAcademy/base")
			for b_f in base_files:
				os.system("cd ./temp_openjk/install/JediAcademy/base ; mv " + b_f.replace(" ","\ ") + " " + game_data_dir.replace(" ","\ ") + "base/" + " ; cd ../../../../")
		else:
			os.system("cd ./temp_openjk/install/JediAcademy/ ; mv " + jk_f.replace(" ","\ ") + " " + game_data_dir.replace(" ","\ ") + " ; cd ../../../")

	# Install Movie Battles
	temp = doc.xpath('//a/@href')
	links = []
	for t in temp:
		if "drive.google" in t:
			links += [t]

	print(links)
	update_link = links[0]
	file_id = update_link.split("/view")
	update_link = file_id[0]
	file_id = update_link.split("/")[-1]
	update_link = "https://drive.google.com/u/0/uc?id=" + file_id + "&export=download"

	print("Downloading Movie Battles 2...")
	os.system("mkdir temp_patch")
	download_file_from_google_drive(update_link,file_id, "./temp_patch/patch.zip")
	print("Unpacking patch...")
	os.system("cd temp_patch ; unzip patch.zip ; cd ../")
	os.system("cd temp_patch ; rm *.bat ; cd ../")
	os.system("cd temp_patch ; rm *.dll ; cd ../")
	os.system("cd temp_patch ; rm *.exe ; cd ../")
	mb_files = os.listdir("./temp_patch")
	for mb_f in mb_files:
		if mb_f == "patch.zip":
			continue
		os.system("cd ./temp_patch ; mv " + mb_f.replace(" ","\ ") + " " + game_data_dir.replace(" ","\ ") + " ; cd ../")	

	os.system("rm -rf temp_patch ; rm -rf temp_openjk")



if __name__ == "__main__":

	movie_battles_url = "https://community.moviebattles.org/pages/download/#manual"
	print(title)
	print(name)
	install = False
	usage = "To update the game: python mb_update.py --dir=<path to Jedi Academy Game Data directory> \nTo install the game: python mb_update.py --install --dir=<path to Jedi Academy Game Data directory>"
	req = request.Request(movie_battles_url, headers={
                    'User-Agent' : choice(user_agents),
    })

	r = request.urlopen(req)
	doc = html5lib.parse(r, treebuilder='lxml',namespaceHTMLElements=False)
	temp = doc.xpath('//center/text()')

	for t in temp:
		if "version" in t and "If" not in t:
			version = t.split(" ")[2][:-2]
			break

	game_data_dir = "./"
	for arg in sys.argv:
		if "--dir" in arg:
			game_data_dir = arg.split("=")[-1]
			if game_data_dir[-1] != "/":
				game_data_dir += "/"
		if "--install" in arg:
			install = True

	if(install):
		install_mb(game_data_dir,doc)
	else:
		update(game_data_dir,version,doc)

