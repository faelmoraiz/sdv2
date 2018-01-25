# coding:utf-8
#!/usr/bin/python
#
# Coded by faelmoraiz on 22, jan, 2018
#
#
# 24, jan, updated with classes

from time import sleep as slp
from time import strftime as st
import time, os, random, re, getpass
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options

class InstaFollow:
	def __init__(self, user, passwd):

		self.CE = '\033[0;0m';self.C0 = '\033[90m';self.C1 = '\033[31m'
		self.C2 = '\033[92m' ;self.C3 = '\033[93m';self.C4 = '\033[94m'
		self.C5 = '\033[95m' ;self.C6 = '\033[96m';self.C7 = '\033[97m'
		self.F1 = '\033[41m' ;self.F3 = '\033[43m';self.F4 = '\033[44m'
		self.N4 = '\033[94m'

		self.user = user
		self.passwd = passwd

		self.block_time = 30 * 60
		self.interval = 15 * 60
		self.lag = 1

		self.tempo1=1
		self.tempo2=2
		self.tempo3=4

		with open('comments.lst','r') as comments_file:
			self.comments = comments_file.readlines()

		with open('profiles.lst','r') as profiles_file:
			self.profiles = profiles_file.readlines()

	def driver(self):
		bro = webdriver.Chrome()
		bro.set_window_size(300,500)
		bro.set_window_position(900, 150)
		return bro

	def openinsta(self, bro):
		bro.get('https://www.instagram.com/')
		bro.find_elements(By.XPATH, '//a[text()="Faça login"]')[0].click()

	def login(self, bro):
		bro.find_elements_by_xpath("//input[@class='_ph6vk _jdqpn _o716c']")[0].send_keys(self.user)
		slp(self.tempo1*self.lag)
		bro.find_elements_by_xpath("//input[@class='_ph6vk _jdqpn _o716c']")[1].send_keys(self.passwd)
		slp(self.tempo1*self.lag)
		bro.find_elements(By.XPATH, '//button[text()="Entrar"]')[0].click()
		slp(self.tempo2*self.lag)

	def add(self, bro, page_select):
		pages = page_select[0:20]
		added=1
		for page in pages:
			try:
				bro.get('https://www.instagram.com/' + page + '/')
				slp(self.tempo3*self.lag)
				bro.find_elements_by_xpath("//div[@class='_e3il2']")[0].click()
				slp(self.tempo2*self.lag)
				try:
					bro.find_elements_by_xpath("//a[@class='_nzn1h _gu6vm']")[0].click()
				except: 
					bro.find_elements_by_xpath("//a[@class='_nzn1h']")[0].click()
				slp(self.tempo2*self.lag)
				users = bro.find_elements_by_xpath("//button[@class='_qv64e _gexxb _4tgw8 _njrw0']")
				slp(self.tempo2*self.lag)
				random.shuffle(users)
				for user in users:
					user.click()
					slp(random.randrange(1,4))
					print(self.F1 + st('%H:%M:%S') + self.CE + '[' + str(added) + ']' + self.C4 + '[+] Adicionando usuários...', end='\r');added+=1
			except Exception as add_err:
				print('\nAdicionados:', str(added))
				return
		print('\nAdicionados:', str(added))

	def action(self, bro, page_select):
		x=0
		max=25
		
		for page in page_select:
			if x > max:
				return
			print('\n'+ self.F4 + st('%H:%M:%S') + self.CE + self.C7 +' ['+ self.C2 + str(max-x) + self.C7 +'] Página:', self.N4 + str(page) + self.CE)
			x+=1
			users = []
			try:
				bro.get('https://www.instagram.com/' + page + '/')
				slp(self.tempo3*self.lag)
				# open first post
				bro.find_elements_by_xpath("//div[@class='_e3il2']")[0].click()
				slp(self.tempo3*self.lag)

				comments_post = bro.find_elements_by_xpath("//a[@class='_2g7d5 notranslate _95hvo']")
				
				for comments_list in comments_post:
					user = comments_list.get_attribute("innerHTML")
					if user not in users:
						users.append(user)

				if len(comments_post) < 10:
					print(self.F4 + st('%H:%M:%S') + ' ' + self.C0 + '[!] Poucos comentários.' + self.CE)
					x-=1
					continue
				elif self.user in users:
					print(self.F4 + st('%H:%M:%S') + ' ' + self.N4 + '[!] Já existe um comentário recente seu.' + self.CE)
					x-=1
					continue
				# open comment campo
				bro.find_elements_by_xpath("//a[@class='_p6oxf _6p9ga']")[0].click()
				slp(self.tempo2*self.lag)
				# comment
				bro.find_elements_by_xpath("//textarea[@class='_bilrf']")[0].send_keys(random.choice(self.comments))
				slp(self.tempo2*self.lag)
				# Post comment
				#bro.find_elements(By.XPATH, '//button[text()="Publicar"]').click()
				slp(self.tempo2*self.lag)

				try:
					bloqueados_err = bro.find_elements_by_xpath("//a[@class='_rke62']")
					if len(bloqueados_err) > 0:
						print(self.F4 + st('%H:%M:%S') + self.CE + ' ' + '[!] Comentários temporariamente bloqueados!')
						self.add(bro, page_select)
						for secconds in range(self.block_time * self.lag):
							print(self.F4 + st('%H:%M:%S') + self.CE + ' ' + '[!] Aguardando', str(round(((self.block_time*self.lag)-secconds)/60)), 'minutos.', end='\r')
							slp(1)
						continue
				except Exception as block_err:
					print(self.F1 + st('%H:%M:%S') + ' ' + self.CE + '[!] Erro block_err:', str(block_err))
					pass
				
				print(self.F4 + st('%H:%M:%S') + ' ' + self.C2 + '[!] Comentado com sucesso!' + self.CE)

			except Exception as action_err:
				print(self.F1 + st('%H:%M:%S') + ' ' + self.CE + '[!] Erro in action_err:', str(action_err))

	def load(self):
		while True:
			try:
				bro = self.driver()
				break
			except:
				pass
			slp(self.tempo1*self.lag)

		self.openinsta(bro)
		self.login(bro)

		while True:
			random.shuffle(self.profiles)
			page_select = self.profiles
			
			self.action(bro, page_select)

			for seconds in range(self.interval*self.lag+1):
				restante = str(round(((self.interval*self.lag)-seconds)/60))
				print(self.F4 + st('%H:%M:%S') + ' ' + self.C6 + '[...] Processo concluído! Recomeçando em', str(round(((self.interval*self.lag)-seconds)/60)), str('minuto.' if int(restante) < 2 else 'minutos.') + self.CE, end='\r')
				slp(1)

def main():
	os.system('clear')
	user = input('\033[44m' + st('%H:%M:%S') + ' ' + '[!] Usuário: ' + '\033[0;0m')
	passwd = getpass.getpass('\033[41m' + st('%H:%M:%S') + ' ' + '[!] Senha: ' + '\033[0;0m')
	instafollow = InstaFollow(user, passwd)
	os.system('clear')
	instafollow.load()

if __name__ == '__main__':
	main()
