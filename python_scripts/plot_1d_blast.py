# Example python plotting script for the 1D Sod Shock Tube test

import h5py
import numpy as np
import os
import sys

import matplotlib
matplotlib.rcParams['mathtext.default']='regular'
matplotlib.rcParams['xtick.direction']='in'
matplotlib.rcParams['ytick.direction']='in'
matplotlib.rcParams['xtick.top']=True
matplotlib.rcParams['ytick.right']=True
import matplotlib.pyplot as plt

dnamein='./hdf5/'
dnameout='./png/'

if not os.path.exists(dnameout):
    os.makedirs(dnameout)

DE = 0 # dual energy flag - 1 if the test was run with dual energy


def plot_snapshot(snapshot):
    hdf5_file = './hdf5/'+str(snapshot)+'.h5'
    print(hdf5_file)
    plot_snapshot_file(hdf5_file)


def plot_snapshot_file(hdf5_file):
    f = h5py.File(hdf5_file, 'r')
    head = f.attrs
    nx, ny, nz = head['dims']
    gamma = head['gamma'][0]
    d  = np.array(f['density']) # mass density
    mx = np.array(f['momentum_x']) # x-momentum
    my = np.array(f['momentum_y']) # y-momentum
    mz = np.array(f['momentum_z']) # z-momentum
    E  = np.array(f['Energy']) # total energy density
    vx = mx/d
    vy = my/d
    vz = mz/d
    if DE:
      e  = np.array(f['GasEnergy'])
      p  = e*(gamma-1.0)
      ge = e/d
    else: 
      p  = (E - 0.5*d*(vx*vx + vy*vy + vz*vz)) * (gamma - 1.0)
      ge  = p/d/(gamma - 1.0)

    basename = os.path.basename(hdf5_file)
    print(basename)
    basename, _ = os.path.splitext(basename)
    basename = os.path.join(dnameout, basename)

    plot_figure(nx, d, vx, p, ge, basename=basename)
    f.close()


def plot_figure(nx, d, vx, p, ge, basename='', plotsuffix='.png'):
    fig = plt.figure(figsize=(6,6))

    ax1 = plt.axes([0.1, 0.6, 0.35, 0.35])
    plt.axis([0, nx, 0, 1.1])
    ax1.plot(d, 'o', markersize=2, color='black')
    plt.ylabel('Density')

    ax2 = plt.axes([0.6, 0.6, 0.35, 0.35])
    plt.axis([0, nx, -0.1, 1.1])
    ax2.plot(vx, 'o', markersize=2, color='black')
    plt.ylabel('Velocity')

    ax3 = plt.axes([0.1, 0.1, 0.35, 0.35])
    plt.axis([0, nx, 0, 1.1])
    ax3.plot(p, 'o', markersize=2, color='black')
    plt.ylabel('Pressure')

    ax4 = plt.axes([0.6, 0.1, 0.35, 0.35])
    plt.axis([0, nx, 1.5, 3.7])
    ax4.plot(ge, 'o', markersize=2, color='black')
    plt.ylabel('Internal Energy')

    plt.savefig(basename + plotsuffix, dpi=300);
    plt.close(fig)


if __name__ == "__main__":
    hdf5_files = sys.argv[1:]
    for snapshot_file in hdf5_files:
        plot_snapshot_file(snapshot_file)

