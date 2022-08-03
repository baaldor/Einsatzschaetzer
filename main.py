from team import Team
import ttmath
import itertools
from operator import mul
from functools import cache, reduce
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import RELIEF_FLAT, RELIEF_GROOVE, RELIEF_SOLID, RELIEF_SUNKEN
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
from matplotlib.figure import Figure
import matplotlib.backends._backend_tk as tkagg
import matplotlib as mpl
import tkinter as Tk
from random import Random, randint, random, randrange
import numpy

def prettyPrintToTerminal(k_p, erwartungswert, mindestspielstaerke, probabilityForMinTeamSize, sollspielstaerke, prb_sollspielstaerke_erreicht):
  print("Wahrscheinlichkeit für das Ereignis, dass genau K Spieler Zeit haben;")
  for k,p in k_p:
    print("P(K=" + str(k) + ")=" + str(round(100*p, 1)) + " %")

  print("Wahrscheinlichkeit, dass min. "+ str(sollspielstaerke) + " Spieler Zeit haben: " + str(round(100*prb_sollspielstaerke_erreicht, 1)) + " %")
  print("Wahrscheinlichkeit, dass min. "+ str(mindestspielstaerke) + " Spieler Zeit haben: " + str(round(100*probabilityForMinTeamSize, 1)) + " %")
  print("Erwartungswert: " + str(round(erwartungswert, 1)))

def calculateDensityGraphForPlayerProbabilities(probabilityOfUseForAllPlayers):
  return [(k, ttmath.probability(k, probabilityOfUseForAllPlayers)) for k in range(0,len(probabilityOfUseForAllPlayers)+1)]

def calculateCumulativeDistributionGraph(densityGraph):
  k, p = zip(*densityGraph)
  cumulativeP = itertools.accumulate(p)  
  cumProbabilitiesGraph = [(0,1)]  
  cumProbabilitiesGraph.extend([(k+1,1-cp) for k,cp in zip(k,cumulativeP)])  
  return cumProbabilitiesGraph

def calculateProbabilityForMinTeamSize(densityGraph, minimalTeamSize=3):
  return sum([p for k,p in densityGraph if k>=minimalTeamSize])

def calculateEverything(myTeam:Team):
  myTeam.probabilityOfUseForKPlayers = calculateDensityGraphForPlayerProbabilities(myTeam.probabilityOfUseForAllPlayers)  
  myTeam.expectedValue = ttmath.calculateExpectedValue(myTeam.probabilityOfUseForKPlayers)
  myTeam.probabilityForMinTeamSize = calculateProbabilityForMinTeamSize(myTeam.probabilityOfUseForKPlayers, myTeam.minimalTeamSize)
  myTeam.probabilityForNormalTeamSize = calculateProbabilityForMinTeamSize(myTeam.probabilityOfUseForKPlayers, myTeam.normalTeamSize)
  myTeam.distributionMoreOrEqualKPlayers = calculateCumulativeDistributionGraph(myTeam.probabilityOfUseForKPlayers)

def getNewProbabilityOfUseForAllPlayers():
  return numpy.random.random(numpy.random.randint(low=4,high=10))

def _handleMinimalTeamSizeEvent(window, newValue, myTeam:Team):  
  myTeam.minimalTeamSize = newValue
  myTeam.probabilityForMinTeamSize = calculateProbabilityForMinTeamSize(myTeam.probabilityOfUseForKPlayers, myTeam.minimalTeamSize)  
  #print('Fetched a MinimalTeamSizeEvent -> new value: ' + str(newValue))

def _handleNormalTeamSizeEvent(window, newValue, myTeam):  
  # update spinner for minimal team size
  if window[KEY_MINIMAL_TEAM_SIZE].get() > newValue:
    window[KEY_MINIMAL_TEAM_SIZE].update(value=newValue)
    _handleMinimalTeamSizeEvent(window, newValue, myTeam)

  window[KEY_MINIMAL_TEAM_SIZE].update(values=[x for x in range(1, newValue + 1)])

  myTeam.normalTeamSize = newValue

  # recalculate probability to reach normal team size
  myTeam.probabilityForNormalTeamSize = calculateProbabilityForMinTeamSize(myTeam.probabilityOfUseForKPlayers, myTeam.normalTeamSize)
    
  #print('Fetched a NormalTeamSizeEvent -> new value: ' + str(newValue))

def _handlePlayerEvent(window, event, values, myTeam):
  #update probability of use for that player
  myTeam.probabilityOfUseForPlayer[event] = values[event]
  #(re-)calculate all the different probabilities
  calculateEverything(myTeam)

  prettyPrintToTerminal(myTeam.probabilityOfUseForKPlayers, myTeam.expectedValue, myTeam.minimalTeamSize, myTeam.probabilityForMinTeamSize, myTeam.normalTeamSize, myTeam.probabilityForNormalTeamSize)

KEY_MAXIMAL_TEAM_SIZE = 'spin max team size'
KEY_MINIMAL_TEAM_SIZE = 'spin minimal team size'
KEY_NORMAL_TEAM_SIZE = 'spin normal team size'
KEY_CANVAS = 'canvas'

def main():
  def initGUI():
    col =  [
      [sg.Text(aPlayer), sg.Slider(range=(0.0, .99), resolution=.01, default_value=myTeam.probabilityOfUseForPlayer[aPlayer], orientation='horizontal', enable_events=True, key=aPlayer)] for aPlayer in myTeam.players
      ]

    layout = [
      [
        sg.Frame(
          layout = [[
            sg.Text('Number of available Players:'), sg.Spin([x for x in range(1, myTeam.maxTeamSize + 1)], myTeam.defaultTeamSize, key=KEY_MAXIMAL_TEAM_SIZE, enable_events=True),
            sg.Text('Normal Team Size:'), sg.Spin([x for x in range(1, myTeam.defaultTeamSize + 1)], myTeam.normalTeamSize, key=KEY_NORMAL_TEAM_SIZE, enable_events=True),
            sg.Text('Minimal Team Size:'), sg.Spin([x for x in range(1, myTeam.normalTeamSize + 1)], myTeam.minimalTeamSize, key=KEY_MINIMAL_TEAM_SIZE, enable_events=True)
          ]],
          relief=RELIEF_GROOVE,
          title="Options",
          expand_x=True,
          vertical_alignment="Center",
          element_justification="Center"        
        )
      ],
      [
        sg.Column(col), 
        sg.Canvas(size=(640, 480), key=KEY_CANVAS)
      ]
    ]
      
    # create the window and show it without the plot
    window = sg.Window('Einsatzschätzer', layout, finalize=True)

    # needed to access the canvas element prior to reading the window
    canvas_elem = window['canvas']
    
    fig = Figure()

    ax = fig.add_subplot(111)
    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")
    #ax.grid()

    graph = FigureCanvasTkAgg(fig, master=canvas_elem.TKCanvas)
    canvas = canvas_elem.TKCanvas

    return window, ax, graph, canvas, fig
  
  def drawTeamData():    
    ax.cla()    
    ax.yaxis.set_major_formatter(mpl.ticker.PercentFormatter(xmax=1))
    ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(.1))
    ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(1))      
    ax.set_ylim([0, 1.05])

    x_values, y_values = zip(*myTeam.probabilityOfUseForKPlayers)
    gg,y2_values = zip(*myTeam.distributionMoreOrEqualKPlayers)

    ax.bar(x_values, y_values, color='purple')
    ax.step(gg, y2_values, color='blue', where='post', marker=mpl.markers.MarkerStyle(marker="o", fillstyle="none"))
    ax.axvline(myTeam.expectedValue, linestyle="--", color='cornflowerblue', alpha=0.75)
    ax.annotate(
      'Expected Value = %.1f' % myTeam.expectedValue, 
      xy=(myTeam.expectedValue, 1), 
      xycoords=("data", "axes fraction"),
      xytext=(-50,10), 
      textcoords='offset points', 
      bbox=dict(boxstyle="round", facecolor="cornflowerblue", alpha=0.75)
      )
    ax.axhline(myTeam.probabilityForMinTeamSize, linestyle="--", color='orange', alpha=0.75)
    ax.annotate(
      #'P(X >= Minimal Team Size) = %.2f' % myTeam.probabilityForMinTeamSize,
      f'{myTeam.probabilityForMinTeamSize:.1%}', 
      xy = (1, myTeam.probabilityForMinTeamSize),
      xycoords=("axes fraction", "data"),
      xytext=(8,0), 
      textcoords='offset points', 
      bbox=dict(boxstyle="round", facecolor="orange", alpha=0.75),
      ha="left",
      va="center"
      )
    ax.axhline(myTeam.probabilityForNormalTeamSize, linestyle="--", color='green', alpha=0.5)
    ax.annotate(
      #'P(X >= Normal Team Size) = %.2f' % prb_sollspielstaerke_erreicht,
      f'{myTeam.probabilityForNormalTeamSize:.1%}', 
      xy = (1, myTeam.probabilityForNormalTeamSize),
      xycoords=("axes fraction", "data"),
      xytext=(8,0), 
      textcoords='offset points', 
      bbox=dict(boxstyle="round", facecolor="green", alpha=0.75),
      ha="left",
      va="center"
      )
    graph.draw()
    figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds
    figure_w, figure_h = int(figure_w), int(figure_h)    
    photo = Tk.PhotoImage(master=canvas, width=figure_w, height=figure_h)
    canvas.create_image(640 / 2, 480 / 2, image=photo)
    figure_canvas_agg = FigureCanvasAgg(fig)
    figure_canvas_agg.draw()  
    tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer,(0, 1, 2, 3))
    return photo    

  myTeam = Team()
  calculateEverything(myTeam)
  window, ax, graph, canvas, fig = initGUI()
  
  # Our event loop        
  while True:
    event, values = window.read(timeout=20)
    if event == sg.WIN_CLOSED:
      break
    elif event in myTeam.players:
      _handlePlayerEvent(window, event, values, myTeam)        
    elif event == KEY_MAXIMAL_TEAM_SIZE:        
      pass
    elif event == KEY_NORMAL_TEAM_SIZE:
      _handleNormalTeamSizeEvent(window, values[KEY_NORMAL_TEAM_SIZE], myTeam)        
    elif event == KEY_MINIMAL_TEAM_SIZE:
      _handleMinimalTeamSizeEvent(window, values[KEY_MINIMAL_TEAM_SIZE], myTeam)

    photo= drawTeamData()

      
  window.close()

if __name__ == "__main__":
  main()