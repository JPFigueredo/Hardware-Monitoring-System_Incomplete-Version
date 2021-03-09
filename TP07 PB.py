import pygame
import psutil
import cpuinfo
import socket
import time
import nmap
from cpuinfo import get_cpu_info

red = (200,0,0)
white = (210,214,217)
blue = (0,0,200)
grey = (105,105,105)
black = (0,0,0)

largura_tela, altura_tela = 1024,760
pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 32)
uso = psutil.cpu_percent(interval=1, percpu=True)    
tela = pygame.display.set_mode((largura_tela, altura_tela))
ip = socket.gethostbyname(socket.gethostname())
info = get_cpu_info()
address = psutil.net_if_addrs()
p = psutil.Process()
processos = psutil.pids()
menu = ""
menu1 = True
menu2 = True
menu3 = True
p_lista = []
pos = pygame.mouse.get_pos()
buttons = 30

pygame.display.set_caption("TP07 - Monitoramento do PC")
pygame.display.init()
clock = pygame.time.Clock()

def pc_infos():
    font = pygame.font.Font(None, 36) 
    s1 = pygame.surface.Surface((largura_tela, altura_tela/3))
    texto_barra = "Detalhes do Processador"
    text = font.render(texto_barra, 1, white)
    s1.blit(text, (30, 10))
    font = pygame.font.Font(None, 28)
    texto_barra = ('Nome: {}'.format(info['brand_raw']))
    text = font.render(texto_barra, 1, white)
    s1.blit(text, (30, 50))
    texto_barra = ('Arquitetura: {}'.format(info['arch_string_raw']))
    text = font.render(texto_barra, 1, white)
    s1.blit(text, (30, 90))
    texto_barra = ('Palavra (bits): {}'.format(info['bits']))
    text = font.render(texto_barra, 1, white)
    s1.blit(text, (30, 120))
    texto_barra = ('Frequência (MHz): {}'.format(round(psutil.cpu_freq().current, 2)))
    text = font.render(texto_barra, 1, white)
    s1.blit(text, (30, 150))
    texto_barra = ('Núcleos (Físicos): {} ({})'.format(psutil.cpu_count(), psutil.cpu_count(logical=False)))
    text = font.render(texto_barra, 1, white)
    s1.blit(text, (30, 180))
    y = 60
    for chave in address:
        IP = address[chave][1]
        addrs = IP[:3]
        y+= 30
        texto_barra = ('{:12.10}: {} - netmask: {}'.format(chave, addrs[1], addrs[2]))
        text = font.render(texto_barra, 1, white)
        s1.blit(text, (350, y))
        tela.blit(s1, (0, 0))


def cpu_graph():
    s2 = pygame.surface.Surface((largura_tela, altura_tela/5))
    uso = psutil.cpu_percent(interval=1)
    larg = largura_tela - 2*40
    pygame.draw.rect(s2, blue, (20, 30, larg, 10))
    larg = larg*uso/100
    pygame.draw.rect(s2, red, (20, 30, larg, 10))
    texto_barra = 'Uso de CPU: {}%'.format(uso)
    text = font.render(texto_barra, 1, white)
    s2.blit(text, (20, 0))
    tela.blit(s2, (0, 250))
    
    
def m_graph():    
    s3 = pygame.surface.Surface((largura_tela, altura_tela/5))    
    m = psutil.virtual_memory()
    larg = largura_tela - 2*40
    pygame.draw.rect(s3, blue, (20, 30, larg, 10))  
    larg = larg*m.percent/100
    pygame.draw.rect(s3, red, (20, 30, larg, 10))
    total = round(m.total/(1024*1024*1024),2)
    texto_barra = 'Uso de Memória: {}% (Total: {} GB)'.format(m.percent, total)
    text = font.render(texto_barra, 1, white)
    s3.blit(text, (20, 0))
    tela.blit(s3, (0, 350))
    
    
def disk_graph():
    s4 = pygame.surface.Surface((largura_tela, altura_tela/5))
    disk = psutil.disk_usage('.')
    larg = largura_tela - 2*40
    pygame.draw.rect(s4, blue, (20, 30, larg, 10))
    larg = larg*disk.percent/100
    pygame.draw.rect(s4, red, (20, 30, larg, 10))
    total = round(disk.total/(1024*1024*1024), 2)
    texto_barra = 'Uso de Disco: {}% (Total: {} GB):'.format(disk.percent,total)
    text = font.render(texto_barra, 1, white)
    s4.blit(text, (20, 0))
    tela.blit(s4, (0, 450))
    

def threads_graph():
    s5 = pygame.surface.Surface((largura_tela, altura_tela))
    y = 10
    num_cpu = len(uso)
    desl = 9
    d = y + desl
    for i in range(num_cpu):
        alt = s5.get_height() - 2*y
        larg = (alt - (num_cpu+1)*desl)/num_cpu
        pygame.draw.rect(s5, red, (d, y, larg, alt))
        pygame.draw.rect(s5, blue, (d, y, larg, (alt*uso[i]/100)))
        d = d + larg + desl
        tela.blit(s5, (0, 550))
        
def threads_text():
    s5 = pygame.surface.Surface((largura_tela, altura_tela))
    texto_barra = 'Uso de Threads:'.format()
    text = font.render(texto_barra, 1, white)
    s5.blit(text, (20, 0))
    tela.blit(s5, (0, 530))


def infos():
    s1 = pygame.surface.Surface((largura_tela, altura_tela))
    font = pygame.font.Font(None, 36)
    texto_barra = "Monitoramento de Uso"
    text = font.render(texto_barra, 1, white)
    s1.blit(text, (350, 10))
    font = pygame.font.Font(None, 28)
    texto_barra = ('Nome: {}'.format(info['brand_raw']))
    text = font.render(texto_barra, 1, white)
    s1.blit(text, (20, 60))
    texto_barra = ('Arquitetura: {}'.format(info['arch_string_raw']))
    text = font.render(texto_barra, 1, white)
    s1.blit(text, (20, 90))
    texto_barra = ('Palavra (bits): {}'.format(info['bits']))
    text = font.render(texto_barra, 1, white)
    s1.blit(text, (20, 120))
    texto_barra = ('Frequência (MHz): {}'.format(round(psutil.cpu_freq().current, 2)))
    text = font.render(texto_barra, 1, white)
    s1.blit(text, (20, 150))
    texto_barra = ('Núcleos (físicos): {} ({})'.format(str(psutil.cpu_count()), str(psutil.cpu_count(logical=False))))
    text = font.render(texto_barra, 1, white)
    s1.blit(text, (20, 180))
    texto_barra = ('IP Address: {}'.format(ip))
    text = font.render(texto_barra, 1, white)
    s1.blit(text, (20, 210))
    font = pygame.font.Font(None, 38)
    #CPU
    uso = psutil.cpu_percent(interval=0)
    texto_barra = ('Uso de CPU:           {}% Usado'.format(uso))
    text = font.render(texto_barra, 1, white)
    s1.blit(text, (230, 275))
    #MEMORIA
    m = psutil.virtual_memory()
    total = round(m.total/(1024*1024*1024), 2)
    texto_barra = ('Uso de Memória:   {}%  (Total: {} GB)'.format(m.percent, total))
    text = font.render(texto_barra, 1, white)
    s1.blit(text, (230, 325))
    #HD
    disco = psutil.disk_usage('.')
    total = round(disco.total/(1024*1024*1024), 2)
    texto_barra = ('Uso de Disco:         {}% (Total: {})'.format(disco.percent, total))
    text = font.render(texto_barra, 1, white)
    s1.blit(text, (230, 375))
    tela.blit(s1, (0, 0))
    #THREADS
    uso2 = psutil.cpu_percent(interval=1, percpu=True)
    y = 0
    x = 0
    for i in range(len(uso2)):
        texto_barra = ('Uso de Thread {} : {}% Usado'.format(i + 1, uso2[i]))
        text = font.render(texto_barra, 1, white)
        s1.blit(text, (20+x, 450+y))
        tela.blit(s1, (0, 0))
        y += 30
        if i == 7:
            x += 500
            y -= 240

def dir_header():
    s1 = pygame.surface.Surface((largura_tela, altura_tela/10))
    font = pygame.font.Font(None, 36)
    texto = '{}'.format("Detalhes de Arquivos/Diretórios")
    text = font.render(texto, 1, white)
    s1.blit(text, (650, 10))
    tela.blit(s1, (0, 0))

def process_header():
    s6 = pygame.surface.Surface((largura_tela, altura_tela/8))
    font = pygame.font.Font(None, 16)
    texto_barra = '{:<6}'.format("PID") + " "
    texto_barra = texto_barra + '{:10}'.format("Threads") + "  "
    texto_barra = texto_barra + '{:30}'.format("Data de Criação") + "        "
    texto_barra = texto_barra + '{:25}'.format("CPU - UT")
#  UT - User Time
#  ST - System Time
    texto_barra = texto_barra + '{:26}'.format("CPU - ST")
    texto_barra = texto_barra + '{:25}'.format("Memory(%)") + "   "
    texto_barra = texto_barra + '{:10}'.format("RSS") + "        "
#  Vss = virtual set size
#  Rss = resident set size
    texto_barra = texto_barra + '{:25}'.format("VMS") + "    "
    texto_barra = texto_barra + '{:20}'.format("Executável")
    text = font.render(texto_barra, 1, white)
    s6.blit(text, (20, 80))
    tela.blit(s6, (0, 0))
      
def arq_dir():
    s1 = pygame.surface.Surface((largura_tela, altura_tela))
    p = psutil.Process()
    font = pygame.font.Font(None, 14)
    y = 100
    for i in processos:
        texto_barra = '{:<6}'.format(i) + " "
        texto_barra = texto_barra + '{:^12}'.format(p.num_threads()) + "        "
        texto_barra = texto_barra + '{:26}'.format(time.ctime(p.create_time()))
        texto_barra = texto_barra + '{:20.2f}'.format(p.cpu_times().user)
        texto_barra = texto_barra + '{:30.2f}'.format(p.cpu_times().system)
        texto_barra = texto_barra + '{:30.2f}'.format(p.memory_percent()) + " MB"
        rss = p.memory_info().rss/1024/1024
        texto_barra = texto_barra + '{:30.2f}'.format(rss) + " MB"
#      Vss = virtual set size
#      Rss = resident set size
        vms = p.memory_info().vms/1024/1024
        texto_barra = texto_barra + '{:15.2f}'.format(vms) + " MB" + "                   "
        texto_barra = texto_barra + '{:15}'.format(p.exe())
        text = font.render(texto_barra, 1, white)
        s1.blit(text, (30, y))
        tela.blit(s1, (0, 0))
        y+= 15
        if y >= 600:
            break
#         if (i % 3 == 0) and (i % 5 == 0):
#             break
def arq_dir_button():
    s1 = pygame.surface.Surface((largura_tela, altura_tela))
    font = pygame.font.Font(None, 32)
    pygame.draw.rect(s1, grey, (20, 30, 125, 30))
    texto_barra = "Próximo"
    text = font.render(texto_barra, 1, white)
    s1.blit(text, (38, 35))
    tela.blit(s1, (670, 670))
    
    
def menu_init():
    s0 = pygame.surface.Surface((largura_tela, altura_tela))
    s0.fill(white)
    font = pygame.font.Font(None, 50)
    texto_barra = ("OPÇOES DE TELA")
    text = font.render(texto_barra, 1, black)
    s0.blit(text, (350, 20))
    tela.blit(s0, (0, 0))
    texto_barra = ("Botão esquerdo do mouse - Gráfico de Uso")
    text = font.render(texto_barra, 1, black)
    s0.blit(text, (70, 140))
    tela.blit(s0, (0, 0))
    texto_barra = ("Botão direito do mouse - Monitoramento de Uso Geral")
    text = font.render(texto_barra, 1, black)
    s0.blit(text, (70, 260))
    tela.blit(s0, (0, 0))
    texto_barra = ("ESPAÇO - Detalhes de Arquivos/Diretórios")
    text = font.render(texto_barra, 1, black)
    s0.blit(text, (70, 380))
    tela.blit(s0, (0, 0))
    texto_barra = ("SHIFT - ESCANEAMENTO DE IP")
    text = font.render(texto_barra, 1, black)
    s0.blit(text, (70, 500))
    tela.blit(s0, (0, 0))
    texto_barra = ("TAB - Voltar a Tela Inicial")
    text = font.render(texto_barra, 1, black)
    s0.blit(text, (70, 620))
    tela.blit(s0, (0, 0))
    
def ping_ip(host):
    s1 = pygame.surface.Surface((largura_tela, altura_tela))
    font = pygame.font.Font(None, 32)
    nmp = nmap.PortScanner()
    nmp.scan(host)
    y = 0
    for proto in nmp[host].all_protocols():
        texto_barra = 'Protocolo : {}'.format(proto)
        text = font.render(texto_barra, 1, white)
        s1.blit(text, (20, 20))
        tela.blit(s1, (0, 0))
        lport = nmp[host][proto].keys()
        for port in lport:
            texto_barra = 'Porta: {:<15}      Estado: {:>10}'.format(port, nmp[host][proto][port]['state'])
            text = font.render(texto_barra, 1, white)
            s1.blit(text, (70, 120+y))
            tela.blit(s1, (0, 0))
            y+= 30


menu_init()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()         
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos_x, pos_y = pygame.mouse.get_pos()
            if pos_x >= 691 and pos_x <= 815 and pos_y >= 700 and pos_y <= 730:
                buttons += 30
            else:
                menu = "menu1"
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            menu = "menu2"
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            menu = "menu3"
        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            menu = ""
            menu_init()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
            ping_ip(ip)
            

    if menu == "menu1":
        pc_infos()        
        cpu_graph()
        m_graph()
        disk_graph()
        threads_text()
        threads_graph()
        if menu != "menu1":
            break
    if menu == "menu2":
        infos()
        if menu != "menu2":
            break
    if menu == "menu3":
        arq_dir()
        process_header()
        dir_header() 
        arq_dir_button()
        time.sleep(0.1)
        if menu != "menu3":
            break
        
    pygame.display.update()  
    clock.tick(50)
pygame.display.quit()