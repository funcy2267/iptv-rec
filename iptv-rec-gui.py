#!/usr/bin/python3
import os
import platform
import tkinter as tk
import tkinter.messagebox as tkmb
from tkinter import DISABLED
from os.path import exists

PlatformName = platform.system()

def main_window():
    root = tk.Tk()
    root.geometry("650x500")
    root.wm_title("iptv-rec GUI")

    #Top frame
    frame_top = tk.Frame()
    frame_top.pack(side='top')

    #Channel name
    ChannelNameLabelFrame = tk.LabelFrame(frame_top, text="Channel name")
    ChannelNameLabelFrame.pack()
    global ChannelNameCheckbuttonVar
    ChannelNameCheckbuttonVar = tk.IntVar()
    ChannelNameCheckbutton = tk.Checkbutton(ChannelNameLabelFrame, var=ChannelNameCheckbuttonVar)
    ChannelNameCheckbutton.grid(row=0, column=0)
    ChannelNameCheckbutton.select()
    global ChannelNameEntry
    ChannelNameEntry = tk.Entry(ChannelNameLabelFrame, width=30)
    ChannelNameEntry.grid(row=0, column=1, padx=10, pady=10)

    #Left frame
    frame_left = tk.Frame()
    frame_left.pack(side='left', padx=20)

    #Mode
    ModeLabelFrame = tk.LabelFrame(frame_left, text="Mode")
    ModeLabelFrame.pack()
    ModeCheckbuttonWidth = 10
    global ModeCheckbuttonServerVar
    ModeCheckbuttonServerVar = tk.IntVar()
    ModeCheckbuttonServer = tk.Checkbutton(ModeLabelFrame, text="Server", width=ModeCheckbuttonWidth, var=ModeCheckbuttonServerVar, state=DISABLED)
    ModeCheckbuttonServer.grid(row=0, column=0)
    ModeCheckbuttonServer.select()
    global ModeCheckbuttonPreviewVar
    ModeCheckbuttonPreviewVar = tk.IntVar()
    ModeCheckbuttonPreview = tk.Checkbutton(ModeLabelFrame, text="Preview", width=ModeCheckbuttonWidth,  var=ModeCheckbuttonPreviewVar)
    ModeCheckbuttonPreview.grid(row=1, column=0)
    ModeCheckbuttonPreview.deselect()
    global ModeCheckbuttonRecordVar
    ModeCheckbuttonRecordVar = tk.IntVar()
    ModeCheckbuttonRecord = tk.Checkbutton(ModeLabelFrame, text="Record", width=ModeCheckbuttonWidth, var=ModeCheckbuttonRecordVar)
    ModeCheckbuttonRecord.grid(row=2, column=0)
    ModeCheckbuttonRecord.deselect()

    #Status
    StatusLabelFrame = tk.LabelFrame(frame_left, text="Status")
    StatusLabelFrame.pack()
    global StatusCheckbuttonEnableFilterVar
    StatusCheckbuttonEnableFilterVar = tk.IntVar()
    StatusCheckbuttonEnableFilter = tk.Checkbutton(StatusLabelFrame, text="Enable filter", var=StatusCheckbuttonEnableFilterVar)
    StatusCheckbuttonEnableFilter.grid(row=0, column=0)
    StatusCheckbuttonEnableFilter.select()
    global StatusVar
    StatusVar = tk.StringVar(None, 'online')
    StatusRadiobuttonOnline = tk.Radiobutton(StatusLabelFrame, text="Online", var=StatusVar, value="online")
    StatusRadiobuttonOnline.grid(row=1, column=0)
    StatusRadiobuttonOffline = tk.Radiobutton(StatusLabelFrame, text="Offline", var=StatusVar, value="offline")
    StatusRadiobuttonOffline.grid(row=1, column=1)

    #Country
    CountryLabelFrame = tk.LabelFrame(frame_left, text="Country")
    CountryLabelFrame.pack()
    global CountryCheckbuttonEnableFilterVar
    CountryCheckbuttonEnableFilterVar = tk.IntVar()
    CountryCheckbuttonEnableFilter = tk.Checkbutton(CountryLabelFrame, text="Enable filter", var=CountryCheckbuttonEnableFilterVar)
    CountryCheckbuttonEnableFilter.grid(row=0, column=0)
    global CountryEntry
    CountryEntry = tk.Entry(CountryLabelFrame, width=25)
    CountryEntry.grid(row=1, column=0, padx=10, pady=10)

    #Liveliness
    LivelinessLabelFrame = tk.LabelFrame(frame_left, text="Liveliness")
    LivelinessLabelFrame.pack()
    global LivelinessCheckbuttonEnableFilterVar
    LivelinessCheckbuttonEnableFilterVar = tk.IntVar()
    LivelinessCheckbuttonEnableFilter = tk.Checkbutton(LivelinessLabelFrame, text="Enable filter", var=LivelinessCheckbuttonEnableFilterVar)
    LivelinessCheckbuttonEnableFilter.grid(row=0, column=0)
    global LivelinessEntry
    LivelinessEntry = tk.Entry(LivelinessLabelFrame, width=5)
    LivelinessEntry.grid(row=0, column=1, padx=10, pady=10)

    #Mbps
    MbpsLabelFrame = tk.LabelFrame(frame_left, text="Mbps")
    MbpsLabelFrame.pack()
    global MbpsCheckbuttonEnableFilterVar
    MbpsCheckbuttonEnableFilterVar = tk.IntVar()
    MbpsCheckbuttonEnableFilter = tk.Checkbutton(MbpsLabelFrame, text="Enable filter", var=MbpsCheckbuttonEnableFilterVar)
    MbpsCheckbuttonEnableFilter.grid(row=0, column=0)
    global MbpsEntry
    MbpsEntry = tk.Entry(MbpsLabelFrame, width=5)
    MbpsEntry.grid(row=0, column=1, padx=10, pady=10)

    #Right frame
    frame_right = tk.Frame()
    frame_right.pack(side='right', padx=20)

    #Autosort
    AutosortLabelFrame = tk.LabelFrame(frame_right, text="Auto-sort")
    AutosortLabelFrame.pack()
    global AutosortCheckbuttonEnableVar
    AutosortCheckbuttonEnableVar = tk.IntVar()
    AutosortCheckbuttonEnable = tk.Checkbutton(AutosortLabelFrame, text="Enable", var=AutosortCheckbuttonEnableVar)
    AutosortCheckbuttonEnable.grid(row=0, column=0)
    global AutosortVar
    AutosortVar = tk.StringVar(None, 'liveliness')
    AutosortRadiobuttonLiveliness = tk.Radiobutton(AutosortLabelFrame, text="Liveliness", var=AutosortVar, value="liveliness")
    AutosortRadiobuttonLiveliness.grid(row=1, column=0)
    AutosortRadiobuttonMbps = tk.Radiobutton(AutosortLabelFrame, text="Mbps", var=AutosortVar, value="mbps")
    AutosortRadiobuttonMbps.grid(row=1, column=1)

    #Output
    OutputLabelFrame = tk.LabelFrame(frame_right, text="Output file")
    OutputLabelFrame.pack()
    global OutputCheckbuttonVar
    OutputCheckbuttonVar = tk.IntVar()
    OutputCheckbutton = tk.Checkbutton(OutputLabelFrame, var=OutputCheckbuttonVar)
    OutputCheckbutton.grid(row=0, column=0)
    global OutputEntry
    OutputEntry = tk.Entry(OutputLabelFrame, width=25)
    OutputEntry.grid(row=0, column=1, padx=10, pady=10)

    #Timeout
    TimeoutLabelFrame = tk.LabelFrame(frame_right, text="Timeout")
    TimeoutLabelFrame.pack()
    global TimeoutCheckbuttonVar
    TimeoutCheckbuttonVar = tk.IntVar()
    TimeoutCheckbutton = tk.Checkbutton(TimeoutLabelFrame, var=TimeoutCheckbuttonVar)
    TimeoutCheckbutton.grid(row=0, column=0)
    global TimeoutEntry
    TimeoutEntry = tk.Entry(TimeoutLabelFrame, width=5)
    TimeoutEntry.grid(row=0, column=1, padx=10, pady=10)

    #Custom link
    LinkLabelFrame = tk.LabelFrame(frame_right, text="Custom link")
    LinkLabelFrame.pack()
    global LinkCheckbuttonVar
    LinkCheckbuttonVar = tk.IntVar()
    LinkCheckbutton = tk.Checkbutton(LinkLabelFrame, var=LinkCheckbuttonVar)
    LinkCheckbutton.grid(row=0, column=0)
    global LinkEntry
    LinkEntry = tk.Entry(LinkLabelFrame, width=20)
    LinkEntry.grid(row=0, column=1, padx=10, pady=10)

    #Server target
    TargetLabelFrame = tk.LabelFrame(frame_right, text="Target")
    TargetLabelFrame.pack()
    global TargetCheckbuttonVar
    TargetCheckbuttonVar = tk.IntVar()
    TargetCheckbutton = tk.Checkbutton(TargetLabelFrame, var=TargetCheckbuttonVar)
    TargetCheckbutton.grid(row=0, column=0)
    global TargetEntry
    TargetEntry = tk.Entry(TargetLabelFrame, width=25)
    TargetEntry.grid(row=0, column=1, padx=10, pady=10)

    #Server port
    PortLabelFrame = tk.LabelFrame(frame_right, text="Port")
    PortLabelFrame.pack()
    global PortCheckbuttonVar
    PortCheckbuttonVar = tk.IntVar()
    PortCheckbutton = tk.Checkbutton(PortLabelFrame, var=PortCheckbuttonVar)
    PortCheckbutton.grid(row=0, column=0)
    global PortEntry
    PortEntry = tk.Entry(PortLabelFrame, width=10)
    PortEntry.grid(row=0, column=1, padx=10, pady=10)

    #Bottom frame
    frame_bottom = tk.Frame()
    frame_bottom.pack(side='bottom')

    StartButton = tk.Button(frame_bottom, text = "Start", command=start_iptv, height=1, width=8)
    StartButton.grid(padx = 3, pady = 3)

    root.mainloop()

def start_iptv():
    args = []
    if ChannelNameCheckbuttonVar.get() == 1:
        args = args + ['--name', ChannelNameEntry.get().replace(' ', '_')]
    if ModeCheckbuttonServerVar.get() == 1:
        args = args + ['--mode', 's']
    if ModeCheckbuttonRecordVar.get() == 1:
        args = args + ['--mode', 'r']
    if ModeCheckbuttonPreviewVar.get() == 1:
        args = args + ['--mode', 'p']
    if StatusCheckbuttonEnableFilterVar.get() == 1:
        args = args + ['--status', StatusVar.get()]
    if CountryCheckbuttonEnableFilterVar.get() == 1:
        args = args + ['--country', CountryEntry.get().replace(' ', '_')]
    if LivelinessCheckbuttonEnableFilterVar.get() == 1:
        args = args + ['--liveliness', LivelinessEntry.get()]
    if MbpsCheckbuttonEnableFilterVar.get() == 1:
        args = args + ['--mbps', MbpsEntry.get()]
    if AutosortCheckbuttonEnableVar.get() == 1:
        args = args + ['--autosort', AutosortVar.get()]
    if OutputCheckbuttonVar.get() == 1:
        args = args + ['--output', OutputEntry.get().replace(' ', '_')]
    if TimeoutCheckbuttonVar.get() == 1:
        args = args + ['--timeout', TimeoutEntry.get()]
    if LinkCheckbuttonVar.get() == 1:
        args = args + ['--link', LinkEntry.get()]
    if TargetCheckbuttonVar.get() == 1:
        args = args + ['--target', TargetEntry.get()]
    if PortCheckbuttonVar.get() == 1:
        args = args + ['--port', PortEntry.get()]

    if AutosortCheckbuttonEnableVar.get() == 0:
        tk.messagebox.showinfo('Information', 'Check console and select stream.')

    iptvrec = 'iptv-rec.py'
    if PlatformName == 'Linux':
        PYTHON_BIN = 'python3'
        pre_cmd = [PYTHON_BIN, iptvrec]
    if PlatformName == 'Windows':
        if exists(iptvrec):
            PYTHON_BIN = 'py'
            pre_cmd = [PYTHON_BIN, iptvrec]
        else:
            iptvrec = '.\\iptv-rec.exe'
            pre_cmd = [iptvrec]
    command = ' '.join(pre_cmd+args)
    os.system(command)

main_window()
