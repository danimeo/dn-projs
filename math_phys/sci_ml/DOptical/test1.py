import clr, os, winreg
from itertools import islice

import matplotlib.pyplot as plt
import numpy as np

import random
import math

import gym
import numpy as np
import sounddevice as sd
from gym import spaces
from stable_baselines3.ddpg.ddpg import DDPG

# This boilerplate requires the 'pythonnet' module.
# The following instructions are for installing the 'pythonnet' module via pip:
#    1. Ensure you are running a Python version compatible with PythonNET. Check the article "ZOS-API using Python.NET" or
#    "Getting started with Python" in our knowledge base for more details.
#    2. Install 'pythonnet' from pip via a command prompt (type 'cmd' from the start menu or press Windows + R and type 'cmd' then enter)
#
#        python -m pip install pythonnet

class PythonStandaloneApplication(object):
    class LicenseException(Exception):
        pass
    class ConnectionException(Exception):
        pass
    class InitializationException(Exception):
        pass
    class SystemNotPresentException(Exception):
        pass

    def __init__(self, path=None):
        # determine location of ZOSAPI_NetHelper.dll & add as reference
        aKey = winreg.OpenKey(winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER), r"Software\Zemax", 0, winreg.KEY_READ)
        zemaxData = winreg.QueryValueEx(aKey, 'ZemaxRoot')
        NetHelper = os.path.join(os.sep, zemaxData[0], r'ZOS-API\Libraries\ZOSAPI_NetHelper.dll')
        winreg.CloseKey(aKey)
        clr.AddReference(NetHelper)
        import ZOSAPI_NetHelper
        
        # Find the installed version of OpticStudio
        #if len(path) == 0:
        if path is None:
            isInitialized = ZOSAPI_NetHelper.ZOSAPI_Initializer.Initialize()
        else:
            # Note -- uncomment the following line to use a custom initialization path
            isInitialized = ZOSAPI_NetHelper.ZOSAPI_Initializer.Initialize(path)
        
        # determine the ZOS root directory
        if isInitialized:
            dir = ZOSAPI_NetHelper.ZOSAPI_Initializer.GetZemaxDirectory()
        else:
            raise PythonStandaloneApplication.InitializationException("Unable to locate Zemax OpticStudio.  Try using a hard-coded path.")

        # add ZOS-API referencecs
        clr.AddReference(os.path.join(os.sep, dir, "ZOSAPI.dll"))
        clr.AddReference(os.path.join(os.sep, dir, "ZOSAPI_Interfaces.dll"))
        import ZOSAPI

        # create a reference to the API namespace
        self.ZOSAPI = ZOSAPI

        # create a reference to the API namespace
        self.ZOSAPI = ZOSAPI

        # Create the initial connection class
        self.TheConnection = ZOSAPI.ZOSAPI_Connection()

        if self.TheConnection is None:
            raise PythonStandaloneApplication.ConnectionException("Unable to initialize .NET connection to ZOSAPI")

        self.TheApplication = self.TheConnection.CreateNewApplication()
        if self.TheApplication is None:
            raise PythonStandaloneApplication.InitializationException("Unable to acquire ZOSAPI application")

        if self.TheApplication.IsValidLicenseForAPI == False:
            raise PythonStandaloneApplication.LicenseException("License is not valid for ZOSAPI use")

        self.TheSystem = self.TheApplication.PrimarySystem
        if self.TheSystem is None:
            raise PythonStandaloneApplication.SystemNotPresentException("Unable to acquire Primary system")

    def __del__(self):
        if self.TheApplication is not None:
            self.TheApplication.CloseApplication()
            self.TheApplication = None
        
        self.TheConnection = None
    
    def OpenFile(self, filepath, saveIfNeeded):
        if self.TheSystem is None:
            raise PythonStandaloneApplication.SystemNotPresentException("Unable to acquire Primary system")
        self.TheSystem.LoadFile(filepath, saveIfNeeded)

    def CloseFile(self, save):
        if self.TheSystem is None:
            raise PythonStandaloneApplication.SystemNotPresentException("Unable to acquire Primary system")
        self.TheSystem.Close(save)

    def SamplesDir(self):
        if self.TheApplication is None:
            raise PythonStandaloneApplication.InitializationException("Unable to acquire ZOSAPI application")

        return self.TheApplication.SamplesDir

    def ExampleConstants(self):
        if self.TheApplication.LicenseStatus == self.ZOSAPI.LicenseStatusType.PremiumEdition:
            return "Premium"
        elif self.TheApplication.LicenseStatus == self.ZOSAPI.LicenseStatusType.EnterpriseEdition:
            return "Enterprise"
        elif self.TheApplication.LicenseStatus == self.ZOSAPI.LicenseStatusType.ProfessionalEdition:
            return "Professional"
        elif self.TheApplication.LicenseStatus == self.ZOSAPI.LicenseStatusType.StandardEdition:
            return "Standard"
        elif self.TheApplication.LicenseStatus == self.ZOSAPI.LicenseStatusType.OpticStudioHPCEdition:
            return "HPC"
        else:
            return "Invalid"
    
    def reshape(self, data, x, y, transpose = False):
        """Converts a System.Double[,] to a 2D list for plotting or post processing
        
        Parameters
        ----------
        data      : System.Double[,] data directly from ZOS-API 
        x         : x width of new 2D list [use var.GetLength(0) for dimension]
        y         : y width of new 2D list [use var.GetLength(1) for dimension]
        transpose : transposes data; needed for some multi-dimensional line series data
        
        Returns
        -------
        res       : 2D list; can be directly used with Matplotlib or converted to
                    a numpy array using numpy.asarray(res)
        """
        if type(data) is not list:
            data = list(data)
        var_lst = [y] * x;
        it = iter(data)
        res = [list(islice(it, i)) for i in var_lst]
        if transpose:
            return self.transpose(res);
        return res
    
    def transpose(self, data):
        """Transposes a 2D list (Python3.x or greater).  
        
        Useful for converting mutli-dimensional line series (i.e. FFT PSF)
        
        Parameters
        ----------
        data      : Python native list (if using System.Data[,] object reshape first)    
        
        Returns
        -------
        res       : transposed 2D list
        """
        if type(data) is not list:
            data = list(data)
        return list(map(list, zip(*data)))


def analyze(TheApplication, TheSystem, TheLDE, newWin, radius, thickness, material, aperture):
    
    surf = []
    for i in range(len(radius)):
        sf = TheLDE.GetSurfaceAt(i + 1)
        sf.Thickness = thickness[i]
        sf.Radius = radius[i]
        sf.Material = material[i]
        surf.append(sf)
    
    #! [e01s07_py]
    # Solver
    Solver = surf[-1].RadiusCell.CreateSolveType(ZOSAPI.Editors.SolveType.FNumber)
    SolverFNumber = Solver._S_FNumber
    SolverFNumber.FNumber = 10
    surf[-1].RadiusCell.SetSolveData(Solver)
    
    # QuickFocus
    quickFocus = TheSystem.Tools.OpenQuickFocus()
    quickFocus.Criterion =  ZOSAPI.Tools.General.QuickFocusCriterion.SpotSizeRadial
    quickFocus.UseCentroid = True
    quickFocus.RunAndWaitForCompletion()
    quickFocus.Close()
    
    # Settings
    newWin_Settings = newWin.GetSettings()
    newWin_Settings.MaximumFrequency = 80
    newWin_Settings.SampleSize = ZOSAPI.Analysis.SampleSizes.S_256x256

    # Run Analysis
    newWin.ApplyAndWaitForCompletion()
    # Get Analysis Results
    newWin_Results = newWin.GetResults()

    # Read and plot data series
    # NOTE: numpy functions are used to unpack and plot the 2D tuple for Sagittal & Tangential MTF
    # You will need to import the numpy module to get this part of the code to work
    colors = ('b','g','r','c', 'm', 'y', 'k')
    outdata = np.zeros((newWin_Results.NumberOfDataSeries * 2,))
    for seriesNum in range(0,newWin_Results.NumberOfDataSeries, 1):
        data = newWin_Results.GetDataSeries(seriesNum)
        
        # get raw .NET data into numpy array
        xRaw = data.XData.Data
        yRaw = data.YData.Data
 
        x = list(xRaw)
        y = zos.reshape(yRaw, yRaw.GetLength(0), yRaw.GetLength(1), True)
        
        plt.plot(x,y[0],color=colors[seriesNum])
        plt.plot(x,y[1],linestyle='--',color=colors[seriesNum])    
        print(x[20], y[0][20], y[1][20])
        outdata[seriesNum * 2] = y[0][20]
        outdata[seriesNum * 2 + 1] = y[1][20]
    return outdata

    # If you want to use numpy, you can replace the last 4 commands in the for loop with:
    #     x = np.array(tuple(xRaw))
    #     y = np.array(np.asarray(tuple(yRaw)).reshape(data.YData.Data.GetLength(0), data.YData.Data.GetLength(1)))
    #    
    #     plt.plot(x[:],y[:,0],color=colors[seriesNum])
    #     plt.plot(x[:],y[:,1],linestyle='--',color=colors[seriesNum])
        
    # # format the plot
    # plt.title('FFT MTF: ' + os.path.basename(testFile))
    # plt.xlabel('Spatial Frequency in cycles per mm')
    # plt.ylabel('Modulus of the OTF')
    # plt.legend([r'$0^\circ$ tangential',r'$0^\circ$ sagittal',r'$14^\circ$ tangential',r'$14^\circ$ sagittal',r'$20^\circ$ tangential',r'$20^\circ$ sagittal'])
    # plt.grid(True)
    
    # # place plt.show() after clean up to release OpticStudio from memory
    # plt.show()
    
    # # Save and close
    # # TheSystem.Save()
    
    
class Simulator(gym.Env):
    def __init__(self, TheApplication, TheSystem, TheLDE, newWin, radius, thickness, material, aperture):
        self.action_space = spaces.Box(high=1., low=-1., shape=(1, 8))
        self.observation_space = spaces.Box(high=1., low=-1., shape=(1, 8))
        self.step_count = 0
        self.TheApplication = TheApplication
        self.TheSystem = TheSystem
        self.TheLDE = TheLDE
        self.newWin = newWin
        self.radius = radius
        self.thickness = thickness
        self.material = material
        self.aperture = aperture
        ra, th = np.array([radius[1:-1]]), np.array([thickness[1:-1]])
        ra = np.clip(ra, -1000, 1000) / 1000.
        th = np.clip(th, 0, 20) / 20.
        # print(np.vstack([ra, th]).shape)
        self.state = np.vstack([ra, th]).reshape((1, 8))
        self.last_ret = 0

    def step(self, action):
        if len(action.shape) != 2:
            action = action.reshape((1, 8))
        outdata = analyze(self.TheApplication, self.TheSystem, self.TheLDE, self.newWin, (action[0, :4] * 1000).tolist(), (action[0, 4:] * 20).tolist(), self.material, self.aperture)
        print(outdata.tolist())
        ret = max(1e-6, float(np.sum(outdata)))
        done = False
        reward = ret
        # if abs(ret - self.last_ret) < 1e-2:
        #     done = True
        self.last_ret = ret
        
        self.state = action
        self.step_count += 1
        print('[第{}轮训练]'.format(self.step_count), 'state:', (action[0, :4] * 1000).tolist(), (action[0, 4:] * 20).tolist())
        print('ret:', ret, 'reward:', reward)
        
        info = {}
        return self.state, reward, done, info

    def reset(self):
        ra, th = np.array([radius[1:-1]]), np.array([thickness[1:-1]])
        ra = np.clip(ra, -1000, 1000) / 1000.
        th = np.clip(th, 0, 20) / 20.
        # print(np.vstack([ra, th]).shape)
        self.state = np.vstack([ra, th]).reshape((1, 8))
        self.last_ret = 0
        return self.state
        # state = np.zeros((6,))
        # return state

    def render(self, mode='human'):
        pass

    def seed(self, seed=None):
        pass


if __name__ == '__main__':
    zos = PythonStandaloneApplication()
    
    # load local variables
    ZOSAPI = zos.ZOSAPI
    TheApplication = zos.TheApplication
    TheSystem = zos.TheSystem
    
    # Insert Code Here
    TheSystem.New(False)
    
    radius = [0, 48.135209, -49.487523, 14.736591, -58.096546, 0]
    thickness = [100.000000, 2.026799, 12.056468, 4.949522, 11.050545, 0]
    material = ['', 'PSK52', '', 'BAF3', '', '']
    aperture = 8.925000
    
    TheSystem.SystemData.MaterialCatalogs.AddCatalog('SCHOTT')
    
    # Aperture
    TheSystemData = TheSystem.SystemData
    TheSystemData.Aperture.ApertureValue = aperture

    # Fields
    # Field_1 = TheSystemData.Fields.GetField(1)
    NewField_2 = TheSystemData.Fields.AddField(0, 2.5, 1.0)

    # Wavelength preset
    slPreset = TheSystemData.Wavelengths.SelectWavelengthPreset(ZOSAPI.SystemData.WavelengthPreset.d_0p587)

    # Lens data
    TheLDE = TheSystem.LDE
    for i in range(len(radius) - 2):
        TheLDE.InsertNewSurfaceAt(2)
    
    # Create analysis
    TheAnalyses = TheSystem.Analyses
    newWin = TheAnalyses.New_FftMtf()
    
    env = Simulator(TheApplication, TheSystem, TheLDE, newWin, radius, thickness, material, aperture)

    model = DDPG(policy="MlpPolicy", env=env, batch_size=8, buffer_size=100000, learning_starts=1)
    
    for _ in range(10):
        obs = env.reset()
        model.learn(total_timesteps=100)
        model.save(r'B:\codes\ds\DOptical\pg_rl.zip')
        print(env.state[:4]*1000, env.state[4:]*20)
        
    # obs = env.reset()
    # # 验证十次
    # for _ in range(10):
    #     action, state = model.predict(observation=obs)
    #     obs = env.reset()
    #     print(action[:10])
    #     obs, reward, done, info = env.step(action)
    #     print(obs[:4]*1000, obs[4:]*20)
    #     env.render()

    # This will clean up the connection to OpticStudio.
    # Note that it closes down the server instance of OpticStudio, so you for maximum performance do not do
    # this until you need to.
    del zos
    zos = None