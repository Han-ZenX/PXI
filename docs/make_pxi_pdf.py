from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase.pdfmetrics import stringWidth

OUT = 'docs/PXI平台概览_文字矢量图.pdf'
FONT = r'C:\Windows\Fonts\msyh.ttf'
pdfmetrics.registerFont(TTFont('CN', FONT))
W, H = landscape(A4)
c = canvas.Canvas(OUT, pagesize=(W, H), pageCompression=1)
c.setTitle('PXI平台概览｜文字矢量图')
NAVY, BLUE, CYAN, INK = HexColor('#10243A'), HexColor('#1769AA'), HexColor('#18A6B7'), HexColor('#203449')
PALE, LINE = HexColor('#F1F6FA'), HexColor('#D8E3EC')

def text(x,y,s,size=9,color=INK,font='CN'):
    c.setFont(font,size); c.setFillColor(color); c.drawString(x,y,s)
def wrap(s, x, y, width, size=8.5, leading=12, color=INK):
    words=list(s); line=''; c.setFont('CN',size); c.setFillColor(color)
    for ch in words:
        if stringWidth(line+ch,'CN',size)>width:
            c.drawString(x,y,line); y-=leading; line=ch
        else: line+=ch
    if line: c.drawString(x,y,line); y-=leading
    return y
def card(x,y,w,h,title,body,accent=BLUE):
    c.setFillColor(white); c.setStrokeColor(LINE); c.roundRect(x,y,w,h,9,fill=1,stroke=1)
    c.setFillColor(accent); c.roundRect(x,y+h-5,w,5,2,fill=1,stroke=0)
    text(x+12,y+h-23,title,11,NAVY)
    yy=y+h-41
    for paragraph in body.split('\n'):
        yy=wrap(paragraph,x+12,yy,w-24,8.2,11)
        yy-=3

c.setFillColor(NAVY); c.rect(0,H-95,W,95,fill=1,stroke=0)
text(34,H-43,'PXI 平台概览',25,white)
text(35,H-66,'模块化测量与自动化系统｜以软件为核心的坚固型 PC 平台',10,HexColor('#C7D9E8'))
text(W-235,H-42,'文字矢量图  ·  内容摘要',9,HexColor('#C7D9E8'))

# Platform architecture strip
text(34,H-122,'系统架构',13,NAVY)
labels=[('软件与测试管理','LabVIEW · Python · C/C++ · .NET · TestStand'),('控制器','嵌入式 / 远程 · Windows / 实时系统'),('机箱与背板','PCI Express · 供电 / 冷却 · 时钟 / 触发'),('仪器模块','DAQ · 示波器 · RF · 开关 · SMU · 数字 I/O')]
gap=10; x0=34; y0=H-198; bw=(W-68-3*gap)/4
for i,(t,b) in enumerate(labels):
    x=x0+i*(bw+gap); c.setFillColor(PALE); c.roundRect(x,y0,bw,57,8,fill=1,stroke=0)
    text(x+11,y0+36,t,10,BLUE); text(x+11,y0+17,b,7.1,INK)
    if i<3:
        c.setStrokeColor(CYAN); c.setLineWidth(1.5); c.line(x+bw+2,y0+28,x+bw+gap-3,y0+28)
        c.line(x+bw+gap-7,y0+32,x+bw+gap-3,y0+28); c.line(x+bw+gap-7,y0+24,x+bw+gap-3,y0+28)

margin=34; gutter=12; col=(W-2*margin-gutter)/2; top=y0-16
card(margin,top-112,col,112,'机箱｜系统骨架',
     '提供电源、冷却、通信背板与多插槽扩展；常见规格为 4–18 槽。PXI Express结合PCIe交换结构，可为设备提供专用数据通道。\n带宽随代际与链路宽度提升；NI页面列出系统吞吐量最高可达 24 GB/s。')
card(margin+col+gutter,top-112,col,112,'定时与同步｜协同测量',
     'PXI提供10 MHz参考时钟、触发总线、星形触发与槽间本地总线。PXI Express增加100 MHz差分时钟与差分同步能力。\n多机箱可通过参考时钟、GPS、IEEE 1588或IRIG等方式协调测量。',CYAN)
card(margin,top-239,col,112,'控制器｜计算与连接',
     '嵌入式控制器把计算能力集成在机箱内；远程控制方案可连接台式机、服务器或笔记本。系统可运行Windows、NI Linux Real-Time或用户自选环境。\n多机箱可采用菊花链或星形拓扑扩展。')
card(margin+col+gutter,top-239,col,112,'模块与软件｜定义系统功能',
     '模块覆盖直流至毫米波的多类仪器。NI称其提供600多种PXI模块；开放生态还包括多家供应商的产品。\n使用LabVIEW、Python、C/C++开发；InstrumentStudio用于交互式仪器控制，TestStand用于测试执行与流程管理。',CYAN)

y=top-263
c.setFillColor(HexColor('#EAF4FA')); c.roundRect(margin,y-40,W-2*margin,40,7,fill=1,stroke=0)
text(margin+12,y-17,'适用场景',9,BLUE)
text(margin+87,y-17,'制造测试  ·  航空航天与国防  ·  汽车与工业测试  ·  机器监测  ·  高速数据采集  ·  硬件在环',8.5,INK)
text(margin+12,y-32,'选型关注',8,BLUE)
text(margin+87,y-32,'槽位与模块兼容性、总线带宽、功率和散热预算、同步精度、控制器形态及软件实时性。',8.2,INK)
c.setStrokeColor(LINE); c.line(34,25,W-34,25)
text(34,12,'来源：NI《PXI平台概览》中文页面。规格与产品数量按页面表述摘要；具体配置以产品文档为准。',7,HexColor('#607487'))
text(W-210,12,'ni.com/zh-cn/shop/pxi/overview-pxi.html',7,HexColor('#607487'))
c.save()
