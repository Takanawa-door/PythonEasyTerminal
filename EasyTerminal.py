class tk:
    from tkinter import Tk,Entry,Toplevel,Listbox
    from tkinter.scrolledtext import ScrolledText
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
    input_list=[]
class os:
    from os import getcwd,chdir,startfile,popen
    from os.path import isfile,isdir
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
def run_command(command,terminal,commandinput):
    def contiune_command():
        terminal.insert('end','\n')
        terminal.insert('end',f'\n{os.getcwd()}\n','green')
        terminal.insert('end',f'$ ')
        terminal.window_create('end',window=commandinput)
        commandinput.focus_set()#"""
    errortext=f'错误指令"{command.strip()}"。'

    command=str(command)
    terminal_infos.input_list.append(command)
    terminal.config(state='n')

    terminal.delete('end')
    commandinput.delete(0,'end')

    if command.strip()=='':
        terminal.insert('end',command)
    elif os.isfile(command.strip().replace('"','')) or os.isfile(os.getcwd()+command.strip().replace('"','')) or os.isfile(command.strip().replace('"','')+'.exe') or os.isfile(os.getcwd()+command.strip().replace('"','')+'.exe'):
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
        terminal.insert('end',command)
        contiune_command()
    elif len(command.strip())>=2:
        if command[0:2]=='::':
            terminal.insert('end',command)
            contiune_command()
        elif command[0:2]=='cd':
            terminal.insert('end',command)
            try:
                os.chdir(command.strip()[3:])
            except OSError as error:
                terminal.insert('end','\n'+error.args[1]+'\n','red')
            except:
                terminal.insert('end','\n移动工作目录失败。\n','red')
            contiune_command()
        elif len(command.strip())>=3:
            if command.lower().strip()[0:3]=='dir':
                terminal.insert('end',command)
                if command.lower().strip()=='dir':
                    try:
                        terminal.insert('end','\n\n'+os.popen('dir '+os.getcwd()).read())
                    except:
                        pass
                elif len(command.lower().strip())>4:
                    if os.isdir(command.strip()[4:].replace('"','')) or os.isdir(os.getcwd()+command.strip()[4:].replace('"',''))==True:
                        terminal.insert('end','\n\n'+os.popen('dir '+command.strip()[4:]).read())
                else:
                    terminal.insert('end','\n'+errortext)
                contiune_command()
            elif command.lower().strip()[0:3]=='set':
                terminal.delete('end')
                if len(command.lower().strip())>3:
                    if '=' in command[4:]:
                        try:
                            def tovar(varname,varvalue):
                                try:
                                    exec(varname+'='+varvalue,terminal_infos.running_space)
                                except:
                                    terminal.insert('end','\n接收输入失败。','red')
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
                            from traceback import format_exc
                            terminal.insert('end','\n接收输入失败。%s'%format_exc(),'red')
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
                    terminal.insert('end',command)
                    if len(command.strip())>4:
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
                            terminal.insert('end','输出了个寂寞。')
                    elif command.lower().strip()=='echo':
                        terminal.insert('end',command)
                        pass
                    else:
                        terminal.insert('end',command)
                        terminal.insert('end','\n'+errortext)
                    contiune_command()
                elif len(command.strip())>=5:
                    if command.lower().strip()[0:5]=='input':
                        terminal.delete('end')
                        if len(command.lower().strip())>5:
                            if '=' in command[4:]:
                                try:
                                    def tovar(varname,varvalue):
                                        try:
                                            exec(varname+'="'+varvalue.replace('"','\\"')+'"',terminal_infos.running_space)
                                        except:
                                            #from traceback import format_exc
                                            #terminal.insert('end','\n接收输入失败。\n%s'%format_exc(),'red')
                                            terminal.insert('end','\n接收输入失败。','red')
                                        commandinput.bind('<Return>',lambda v=0:run_command(command_input.get(),TerminalText,command_input))
                                        terminal['state']='n'
                                        terminal.insert('end',commandinput.get())
                                        commandinput.delete(0,'end')
                                        terminal.insert('end','\n')
                                        terminal.insert('end',f'\n')
                                        terminal.insert('end',f'{os.getcwd()}::','green')
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
                        elif command.lower().strip()=='input':
                            terminal.insert('end',command)
                            terminal.insert('end','\n')
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
    else:
        terminal.insert('end',command)
        terminal.insert('end','\n'+errortext,'red')
        contiune_command()

    terminal.config(state='d')
    terminal.see('end')
def post_inputlist(inputen):
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

    for temp in terminal_infos.input_list:
        commandlist.insert('end',f'{temp}')

root=tk.Tk()
root.title(f'EasyTerminal {terminal_infos.version}')
icon_for_window(root,'')
root.geometry('645x400')
root.resizable(False,False)

TerminalText=tk.ScrolledText(root,state='d',fg='white',bg='black',insertbackground='white',font=('consolas',13),selectforeground='black',selectbackground='white',takefocus=False)
TerminalText.pack(fill='both',expand='yes')

TerminalText.tag_config('red',foreground='red',selectforeground='#00ffff',selectbackground='#ffffff')
TerminalText.tag_config('green',foreground='green',selectforeground='#ff7eff',selectbackground='#ffffff')
TerminalText.tag_config('blue',foreground='blue',selectforeground='#ffff7e',selectbackground='#ffffff')
TerminalText.tag_config('cyan',foreground='cyan',selectforeground='red',selectbackground='#ffffff')

TerminalText['state']='n'
TerminalText.insert('end',f'EasyTerminal {terminal_infos.version} By {terminal_infos.by}\n')
TerminalText.insert('end',f'{os.getcwd()}\n','green')
TerminalText.insert('end',f'$ ')

command_input=tk.Entry(TerminalText,font=('consolas',13),fg='white',bg='black',insertbackground='white',selectforeground='black',selectbackground='white',relief='flat',width=66)
command_input.bind('<Return>',lambda v=0:run_command(command_input.get(),TerminalText,command_input))
command_input.bind('<F7>',lambda v=0:post_inputlist(command_input))

TerminalText.window_create('end',window=command_input)

TerminalText['state']='d'

root.mainloop()
