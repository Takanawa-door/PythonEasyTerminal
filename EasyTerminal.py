#引入Tkinter
class tk:
    from tkinter import Tk,Entry,Toplevel,Listbox
    from tkinter.scrolledtext import ScrolledText
#配置基本信息
class terminal_infos:
    version='1.0'
    by='Takanawa-door'
    running_space={'__name__':'__console__'}
    exec('''def print(*value):
    return None
def input(*value):
    return None
def set(*value):
    return None
def Back(*value):
    pass
del input,print,set,Back''',running_space)
    input_list=[0]
#引入os库
class os:
    from os import getcwd,chdir,startfile,popen
    from os.path import isfile,isdir
#构建icon_for_window函数
def icon_for_window(tkwindow,filevalue,temofilename='tempicon.ico'):
    try:
        import base64
        tmp = open(temofilename, "wb+")
        tmp.write(base64.b64decode(filevalue))
        tmp.close()
        tkwindow.iconbitmap(temofilename)
        from os import remove
        remove(temofilename)
    except:
        pass
#运行命令
def run_command(command,terminal,commandinput):
	#下一个命令输入刷新函数
    def contiune_command():
        terminal.insert('end','\n')
        terminal.insert('end',f'\n{os.getcwd()}\n','green')
        terminal.insert('end',f'$ ')
        terminal.window_create('end',window=commandinput)
        terminal.see('end')
        commandinput.focus_set()#"""
    errortext=f'错误指令"{command.strip()}"。'

    command=str(command)
    try:
        if command!=terminal_infos.input_list[-1] and command.strip()!='':
            terminal_infos.input_list.append(command)
    except:
        pass
    terminal.config(state='n')

    terminal.delete('end')
    commandinput.delete(0,'end')

	#如果啥也没有输入就复述一遍文本
    if command.strip()=='':
        terminal.insert('end',command)#改成pass也行
    elif os.isfile(command.strip().replace('"','')) or os.isfile(os.getcwd()+command.strip().replace('"','')) or os.isfile(command.strip().replace('"','')+'.exe') or os.isfile(os.getcwd()+command.strip().replace('"','')+'.exe'):#如果是个文件路径
		#尝试打开
        try:
            os.startfile(command.strip().replace('"',''))
        except:
            try:
                os.startfile(os.getcwd()+command.strip().replace('"',''))
            except:
                try:
                    os.startfile(command.strip().replace('"','')+'.exe')
                except:
                    os.startfile(os.getcwd()+command.strip().replace('"','')+'.exe')
		#复述输入命令
        terminal.insert('end',command)
		#刷星
        contiune_command()
    elif len(command.strip())>=2:#如果命令长度大于1
        if command[0:2]=='::':#如果是注释
            terminal.insert('end',command)
            contiune_command()
        elif command[0:2]=='cd':#移动目录
            terminal.insert('end',command)
            try:
                os.chdir(command.strip()[3:])
            except OSError as error:
                terminal.insert('end','\n'+error.args[1]+'\n','red')
            except:
                terminal.insert('end','\n移动工作目录失败。\n','red')
            contiune_command()
        elif len(command.strip())>=3:#如果命令长度大于2
            if command.lower().strip()[0:3]=='dir':#DIR命令
                terminal.insert('end',command)
                if command.lower().strip()=='dir':
                    try:
                        terminal.insert('end','\n\n'+os.popen('dir '+os.getcwd()).read())#获取命令执行返回值(重新定向)
                    except:
                        pass
                elif len(command.lower().strip())>4:
                    if os.isdir(command.strip()[4:].replace('"','')) or os.isdir(os.getcwd()+command.strip()[4:].replace('"',''))==True:
                        terminal.insert('end','\n\n'+os.popen('dir '+command.strip()[4:]).read())
                else:
                    terminal.insert('end','\n'+errortext)
                contiune_command()
            elif command.lower().strip()[0:3]=='set':#赋值变量
                terminal.delete('end')
                if len(command.lower().strip())>3:
                    if '=' in command[4:]:
                        try:
                            def tovar(varname,varvalue):
                                try:
                                    exec(varname+'='+varvalue,terminal_infos.running_space)#在running_space中赋值变量，方便管理
                                except:
                                    terminal.insert('end','\n赋值失败。','red')#如果赋值失败就插入文本，标记'red'(引用'red'这个tag的属性)
                                commandinput.bind('<Return>',lambda v=0:run_command(command_input.get(),TerminalText,command_input))
                                command_input.bind('<Return>',lambda v=0:run_command(command_input.get(),TerminalText,command_input))
                                contiune_command()
                            terminal.insert('end',command)
                            tovar(command[command.index(' ',0)+1:command.index('=',0)],command[command.index('=',0)+1:])
                            #terminal.insert('end','\n%s\n'%(command[command.index('=',0)+1:]),'cyan')
                            #terminal.insert('end',f'$ ')
                            #geten=tk.Entry(terminal,font=('consolas',13),fg='white',bg='black',insertbackground='white',selectforeground='black',selectbackground='white',relief='flat',width=66)
                            #terminal.window_create('end',window=commandinput)
                            #commandinput.bind("<Return>",lambda v=0:tovar(command[command.index(' ',0)+1:command.index('=',0)],command[command.index('=',0)+1:]))
                        except:
                            terminal.insert('end','\n赋值失败。')
                            contiune_command()
                    else:
                        terminal.insert('end',command)
                        terminal.insert('end','\n没有等于号或等于号位置错误。','red')
                        contiune_command()
                else:
                    terminal.insert('end',command)
                    terminal.insert('end','\n'+errortext,'red')
                    contiune_command()
            elif len(command.strip())>=4:
                if command.lower().strip()[0:4]=='echo':
					#输出文本 复述
                    terminal.insert('end',command)
                    if len(command.strip())>4:#如果有内容输出
						#尝试输出
                        try:
                            resultprint=eval('''['''+command[5:]+']',terminal_infos.running_space)
                        except NameError:
                            terminal.insert('end','\n变量不存在。','red')
                            resultprint=['']
                        except SyntaxError:
                            terminal.insert('end','\n语法错误，请使用","或"+"连接。','red')
                            resultprint=['']
                        except:
                            terminal.insert('end','\nERROR。','red')
                            resultprint=['']
                        try:
                            terminal.insert('end','\n')
                            for temp in resultprint:
                                terminal.insert('end',temp)
                        except:
                            terminal.insert('end','无法输出。','red')
                    elif command.lower().strip()=='echo':
                        pass
                    else:
                        terminal.insert('end',command)
                        terminal.insert('end','\n'+errortext)
                    contiune_command()#刷新
                elif len(command.strip())>=5:#如果命令长度大于4
                    if command.lower().strip()[0:5]=='input':#如果要接收输入
                        terminal.delete('end')#删除terminal最后一个字符，但是这里是指Entry控件
                        if len(command.lower().strip())>5:
                            if '=' in command[4:]:#如果等于号在4位置及以后
                                try:
                                    def tovar(varname,varvalue):#定义赋值函数
                                        try:
                                            exec(varname+'="'+varvalue.replace('"','\\"')+'"',terminal_infos.running_space)
                                        except:
                                            #from traceback import format_exc
                                            #terminal.insert('end','\n接收输入失败。\n%s'%format_exc(),'red')
                                            terminal.insert('end','\n接收输入失败。','red')
                                        commandinput.bind('<Return>',lambda v=0:run_command(command_input.get(),TerminalText,command_input))
                                        terminal['state']='n'
										#刷新
                                        terminal.insert('end',commandinput.get())
                                        commandinput.delete(0,'end')
                                        terminal.insert('end','\n')
                                        terminal.insert('end',f'\n')
                                        terminal.insert('end',f'{os.getcwd()}','green')
                                        terminal.insert('end',f'\n')
                                        terminal.insert('end',f'$ ')
                                        terminal.window_create('end',window=commandinput)
                                        commandinput.focus_set()
                                        terminal.see('end')
                                        terminal['state']='d'
                                    terminal.insert('end',command)
                                    terminal.insert('end','\n%s\n'%(command[command.index('=',0)+1:]),'cyan')
                                    terminal.insert('end',f'$ ')
                                    terminal.window_create('end',window=commandinput)
                                    commandinput.bind("<Return>",lambda v=0:tovar(command[command.index(' ',0)+1:command.index('=',0)],commandinput.get()))
                                except:
                                    terminal.insert('end','\n接收输入失败。','red')
                                    contiune_command()
                            else:
                                terminal.insert('end',command)
                                terminal.insert('end','\n没有等于号或等于号位置错误。','red')
                                contiune_command()
                        elif command.lower().strip()=='input':#如果输入内容的小写、去除前尾空格形式就是input
                            terminal.insert('end',command)#插入输入的命令
                            terminal.insert('end','\n')#插入换行符
                            contiune_command()#刷新
                        else:#否则在模拟终端报错
                            terminal.insert('end',command)
                            terminal.insert('end','\n'+errortext,'red')
                            contiune_command()
                    elif command.lower().strip()[0:5]=='pause':#如果命令的小写、去除前尾空格形式
                        terminal.delete('end')#删除Entry控件
                        if len(cmmand.lower().strip())>5:#如果命令长度大于5
							#尝试实现
                            try:
                                def contiune_(key):
                                    commandinput.bind('<Key>','')
                                    commandinput['width']=66
                                    print('de')
                                    commandinput.bind('<Return>',lambda v=0:run_command(command_input.get(),TerminalText,command_input))
                                    terminal['state']='n'#解除不可编辑状态
									#刷新
                                    terminal.insert('end',commandinput.get())
                                    commandinput.delete(0,'end')
                                    terminal.insert('end','\n')
                                    terminal.insert('end',f'\n')
                                    terminal.insert('end',f'{os.getcwd()}','green')
                                    terminal.insert('end',f'\n')
                                    terminal.insert('end',f'$ ')
                                    commandinput.delete(0,'end')
                                    terminal.window_create('end',window=commandinput)
                                    commandinput.focus_set()
                                    terminal.see('end')
                                    terminal['state']='d'
                                terminal.insert('end',command)
                                terminal.insert('end','\n%s'%(command.lstrip()[6:]),'cyan')
                                commandinput['width']=1
                                terminal.window_create('end',window=commandinput)
                                commandinput.bind("<Key>",contiune_)
                            except:#发生错误就pass
                                pass
                        elif command.lower().strip()=='pause':#如果它就是pause：重复上面步骤，但输出内容则是"Press any key to contiune. . ."
                            try:
                                def contiune_(key):
                                    commandinput.bind('<Key>','')
                                    commandinput['width']=66
                                    commandinput.delete(0,'end')
                                    commandinput.bind('<Return>',lambda v=0:run_command(command_input.get(),TerminalText,command_input))
                                    terminal['state']='n'
                                    terminal.insert('end',commandinput.get())
                                    commandinput.delete(0,'end')
                                    terminal.insert('end','\n')
                                    terminal.insert('end',f'\n')
                                    terminal.insert('end',f'{os.getcwd()}','green')
                                    terminal.insert('end',f'\n')
                                    terminal.insert('end',f'$ ')
                                    terminal.window_create('end',window=commandinput)
                                    commandinput.focus_set()
                                    terminal.see('end')
                                    terminal['state']='d'
                                terminal.insert('end',command)
                                terminal.insert('end','\nPress any key to contiune. . .')
                                commandinput['width']=1
                                terminal.window_create('end',window=commandinput)
                                commandinput.bind("<Key>",contiune_)
                            except:
                                pass
                        else:#下面一堆都是如果命令不正确
                            terminal.insert('end',command)
                            terminal.insert('end','\n'+errortext,'red')
                            contiune_command()
                    else:
                        terminal.insert('end',command)
                        terminal.insert('end','\n'+errortext,'red')
                        contiune_command()
                else:
                    terminal.insert('end',command)
                    terminal.insert('end','\n'+errortext,'red')
                    contiune_command()
            else:
                terminal.insert('end',command)
                terminal.insert('end','\n'+errortext,'red')
                contiune_command()
        else:
            terminal.insert('end',command)
            terminal.insert('end','\n'+errortext,'red')
            contiune_command()
    else:
        terminal.insert('end',command)
        terminal.insert('end','\n'+errortext,'red')
        contiune_command()

	#将Text禁用
    terminal.config(state='d')
    terminal.see('end')#转到最后一行
def post_inputlist(inputen):
	#弹出命令列表框
    def setit(setmessage):
        inputen.delete(0,'end')
        inputen.insert('end',setmessage)
        postwin.destroy()
    postwin=tk.Toplevel(root,bg='#ffffff')
    icon_for_window(postwin,'')
    postwin.title('CommandList')
    postwin.geometry('300x200')
    postwin.transient(root)

    commandlist=tk.Listbox(postwin,fg='#800080',selectforeground='white',selectbackground='#800080',font=('terminal',16))
    commandlist.bind('<Return>',lambda v=0:setit(commandlist.get(commandlist.curselection())))
    commandlist.bind('<Right>',lambda v=0:setit(commandlist.get(commandlist.curselection())))
    commandlist.bind('<Left>',lambda v=0:setit(commandlist.get(commandlist.curselection())))
    commandlist.pack(fill='both',expand=1)

	#整数0是为了防止BUG
    for temp in terminal_infos.input_list:
		if temp!=0:
        	commandlist.insert('end',f'{temp}')

root=tk.Tk()#创建TK窗口
root.title(f'EasyTerminal {terminal_infos.version}')#设置标题
icon_for_window(root,'')#通过函数设置图标
root.geometry('645x400')#设置默认大小
root.resizable(False,False)#禁止更改大小

#建设终端滚动文本框
TerminalText=tk.ScrolledText(root,state='d',fg='white',bg='black',insertbackground='white',font=('consolas',13),selectforeground='black',selectbackground='white',takefocus=False)
TerminalText.pack(fill='both',expand='yes')

#设置滚动文框Tag
TerminalText.tag_config('red',foreground='red',selectforeground='#00ffff',selectbackground='#ffffff')
TerminalText.tag_config('green',foreground='green',selectforeground='#ff7eff',selectbackground='#ffffff')
TerminalText.tag_config('blue',foreground='blue',selectforeground='#ffff7e',selectbackground='#ffffff')
TerminalText.tag_config('cyan',foreground='cyan',selectforeground='red',selectbackground='#ffffff')

TerminalText['state']='n'#将文本框状态设为默认"normal"
#插入初始内容
TerminalText.insert('end',f'EasyTerminal {terminal_infos.version} By {terminal_infos.by}\n')
TerminalText.insert('end',f'{os.getcwd()}\n','green')
TerminalText.insert('end',f'$ ')

#新建输入命令框(Entry)
command_input=tk.Entry(TerminalText,font=('consolas',13),fg='white',bg='black',insertbackground='white',selectforeground='black',selectbackground='white',relief='flat',width=66)
command_input.bind('<Return>',lambda v=0:run_command(command_input.get(),TerminalText,command_input))
command_input.bind('<F7>',lambda v=0:post_inputlist(command_input))

TerminalText.window_create('end',window=command_input)#将输入命令框放入文本框最后一个字符的后面

TerminalText['state']='d'#禁用终端文本框

root.mainloop()#循环
