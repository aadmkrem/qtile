# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

from libqtile import hook
import os
import subprocess

# COLORS FOR THE BAR
colors = [
    ["#000000", "#000000"],  #0 черный
    ["#6A6A6A", "#6A6A6A"],  #1 темно-серый
    ["#ff0000", "#ff0000"],  #2 красный
    ["#FF8080", "#FF8080"],  #3 кораловый
    ["#97D59B", "#97D59B"],  #4 зеленый 4
    ["#ffffff", "#ffffff"],  #5 белый
    ["#011E3E", "#011E3E"],  #6 темно-синий
    ["#d5e672", "#d5e672"],  #7 
    ["#78a778", "#78a778"],  #8 
    ["#a69c80", "#a69c80"],  #9 
    ["#938270", "#938270"],  #10 
    ["#786b63", "#786b63"],  #11 
]

#@hook.subscribe.startup_once
#def autostart():
#	home = os.path.expanduser("~/.config/qtile/autostart.sh")
#	subprocess.call([home])



mod = "mod4"
alt= "mod1"
terminal = "tilix"
browser = "google-chrome-stable"

keys = [
    #Мои кнопки
    Key([mod], "b",lazy.spawn("firefox")),
    Key([alt], "Shift_L",  lazy.widget["keyboardlayout"].next_keyboard()),

    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "left", lazy.layout.left(), desc="Фокус влево"),
    Key([mod], "right", lazy.layout.right(), desc="Фокус вправо"),
    Key([mod], "down", lazy.layout.down(), desc="Фокус вверх"),
    Key([mod], "up", lazy.layout.up(), desc="Фокус вниз"),
    Key([mod], "space", lazy.layout.next(), desc="Переставить фокус на следующее окно"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "left", lazy.layout.shuffle_left(), desc="Передвинуть окно влево"),
    Key([mod, "shift"], "right", lazy.layout.shuffle_right(), desc="Передвинуть окно вправо "),
    Key([mod, "shift"], "down", lazy.layout.shuffle_down(), desc="Передвинуть вниз"),
    Key([mod, "shift"], "up", lazy.layout.shuffle_up(), desc="Передвинуть вверх"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "left", lazy.layout.grow_left(), desc="Растянуть окно влево"),
    Key([mod, "control"], "right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"],"Return",lazy.layout.toggle_split(),desc="Toggle between split and unsplit sides of stack",),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "b", lazy.spawn(browser), desc="Launch terminal"),
]

groups = []


group_names = ["1", "2", "3", "4", "5", "6",]
group_labels = ["Web ", "Term ", "Files ", "Code ", "Image ", "Video ",]
group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall",]


for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))


for i in groups:
	keys.extend([
		Key([mod], i.name, lazy.group[i.name].toscreen()),
		Key([mod], "Tab", lazy.screen.next_group()),
		Key([mod, "shift" ], "Tab", lazy.screen.prev_group()),
		#Key(["mod1"], "Tab", lazy.screen.next_group()),
		#Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),
		Key([mod, "shift"], i.name, lazy.window.togroup(i.name) , lazy.group[i.name].toscreen()),
    ])
    
layouts = [
    layout.Columns(margin=3, num_columns=4, insert_position=1, border_focus="#bd93f9", border_normal="#282836", border_width=4),
    #layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
     layout.Bsp(),
     layout.Matrix(),
    layout.MonadTall(),
     layout.MonadWide(),
     layout.RatioTile(),
     layout.Tile(),
     layout.TreeTab(),
     layout.VerticalTile(),
     layout.Zoomy(),
]

widget_defaults = dict(
    font='NovaMono for Powerline',
    fontsize=12,
    padding=3,
    background=colors[5],
)

extension_defaults = widget_defaults.copy()
separator = widget.Sep(size_percent=50, background = colors[6], foreground=colors[5], linewidth =1, padding =3,)


screens = [
    Screen(
        wallpaper="~/.config/qtile/112.png",
        wallpaper_mode="fill",
        top=bar.Bar(
            [
                #widget.Sep(
                 #       linewidth =1,
                  #      padding = 10,
                   #     foreground = colors[14],
                    #    background = colors[14]
                     #   ),
                separator,
                widget.GroupBox(font="FontAwesome",
                        fontsize = 13,
                        margin_y = 3,
                        margin_x = 2,
                        padding_y = 5,
                        padding_x = 4,
                        borderwidth = 5,
                        disable_drag = True,
                        active = colors[5],
                        inactive = colors[1],
                        rounded = True,
                        highlight_method = "block",
                        highlight_color = colors[1],
                        this_screen_border = colors[1],
                        this_current_screen_border = colors[2],
                        foreground = colors[1],
                        background = colors[6]
                        ),
                separator,
                #имя текущего окна
                widget.WindowName(
					   font="Sans",
					   background = colors[6],
					   foreground=colors[5],
                       ),
                    
                #выполнить команду
                widget.Prompt(
						font="Sans",
						background = colors[6],
					    foreground=colors[5]
					    ),
				separator,	    
                widget.CheckUpdates (
						background=colors[6],
						colour_have_updates=colors[4],
						colour_no_updates='ffffff',
						display_format='Upd: {updates}',
						distro = "Debian",
						execute=('tilix apt-show-versions -u -b', 0),
						foreground='#8be9fd',
						no_update_string = 'No Upd',
						#mouse_callbacks={'Button1': lazy.spawn("tilix -e sudo apt upgade && sudo apt update")},
						padding = 0,
						update_interval=3600
						),
                #widget.Net(foreground=colors[3],format='{down}↓↑{up}'),
				#погода
				widget.TextBox(
					text='\uE0B2',
					padding=0,
					fontsize=25,
					background=colors[6],
					foreground=colors[10],
					),
				widget.Wttr(
					   lang="ru",
					   location={"Kremyonki":""},
					   format=" %c %t ",font="UbuntuMono",
					   background = colors[10],
					   foreground=colors[0],
					   units="m",
					   update_interval=3600,),
				
				widget.TextBox(
					text='\uE0B2',
					padding=0,
					fontsize=25,
					background=colors[10],
					foreground=colors[11],
					),
                 #громкость      
				widget.TextBox(
                       text = '', 
                       font = "Sans", 
                       fontsize = 28,
                       background = colors[11], 
                       foreground="70ff70",
                       padding = 0
                       ),
				widget.Volume(
					   background = colors[11],
					   foreground="70ff70",
					   padding=5
					   ),
			
				##раскладка
				
				widget.TextBox(
					text='\uE0B2',
					padding=0,
					fontsize=25,
					background=colors[11],
					foreground=colors[10],
					),
				widget.KeyboardLayout(
						configured_keyboards=['us','ru'],
						font = "Sans", 
						fontsize = 12,
						background = colors[10], 
						foreground = colors[0],
                       	),
				
                	       
				widget.TextBox(
					text='\uE0B2',
					padding=0,
					fontsize=25,
					background=colors[10],
					foreground=colors[9],
					),
				widget.TextBox(
                       text = '  ', 
                       font = "Sans", 
                       fontsize = 20,
                       background = colors[9], 
                       foreground = colors[5],
                       padding = 0
                       ),
				widget.Clock(
					   background = colors[9], 
                       foreground = colors[5],
                       icons_size=20,
                       fontsize = 20,
                       padding =0,
                       mouse_callbacks={'Button1': lazy.spawn("gsimplecal")},
                       ),
                
				widget.CurrentLayoutIcon(
                    custom_icon_paths=["/home/demon/.config/qtile/icons/layouts"],
                    background = colors[9], 
                    foreground = colors[5],
                    scale=0.5,
                    padding=0
                ),
				widget.TextBox(
					text='\uE0B2',
					padding=0,
					fontsize=25,
					background=colors[9],
					foreground=colors[7],
					),
				widget.Systray(
						 
						icon_size = 20,
						background = colors[7],
						),
				widget.TextBox(
					text='\uE0B2',
					padding=0,
					fontsize=25,
					background=colors[7],
					foreground=colors[8],
					),
				              
				
                
				widget.QuickExit(
					default_text = '󰐥',
					countdown_format = '{}',
					 fontsize =30,
                     background = colors[8], 
                     foreground = colors[1],
                     ),
							
            ],

            31,
            margin=[13, 15, 5, 15],
            opacity= 1.0,
        ),
        bottom=bar.Gap(18),
        left=bar.Gap(18),
        right=bar.Gap(18),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]




dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
