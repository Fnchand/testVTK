#!/usr/bin/env python

"""
"""

import vtk


def main():
    colors = vtk.vtkNamedColors()

    fileName = "/home/faisal/Desktop/Python tests/VOI/"

    ren = vtk.vtkRenderer()
    renWin=vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    #vtk.GetRenderWindow().AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    reader = vtk.vtkBMPReader()
    #reader.SetFilePrefix("C:/Users/tia chop/Documents/cttrung/")
    reader.Allow8BitBMPOn()
    reader.SetFilePrefix(fileName)
    reader.SetFilePattern("%s%.08d.bmp")
    reader.SetFileNameSliceOffset(0)
    reader.SetFileNameSliceSpacing(1)
    
    #reader.GetDataScalarType()
    reader.SetDataSpacing(400,400,400)
    reader.SetDataExtent(0,399,0,399,0,399)
    reader.Update()
    colors = vtk.vtkNamedColors()
    colors.SetColor("BkgColor", [51, 77, 102, 255])
    volumeMapper = vtk.vtkGPUVolumeRayCastMapper()
    volumeMapper.SetInputConnection(reader.GetOutputPort())

    volumeColor = vtk.vtkColorTransferFunction()
    volumeColor.AddRGBPoint(500, 1.0, 0.5, 0.3)
    volumeColor.AddRGBPoint(1000, 1.0, 0.5, 0.3)
    volumeColor.AddRGBPoint(1150, 1.0, 1.0, 0.9)

    volumeScalarOpacity = vtk.vtkPiecewiseFunction()
    volumeScalarOpacity.AddPoint(0, 0.00)
    volumeScalarOpacity.AddPoint(500, 0.1)
    volumeScalarOpacity.AddPoint(1500, 0.15)
    volumeScalarOpacity.AddPoint(2150, .9)

    volumeGradientOpacity = vtk.vtkPiecewiseFunction()
    volumeGradientOpacity.AddPoint(10, 0.0)
    volumeGradientOpacity.AddPoint(100, 0.5)
    volumeGradientOpacity.AddPoint(200, 1.0)
    
    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.SetColor(volumeColor)
    volumeProperty.SetScalarOpacity(volumeScalarOpacity)

    volumeProperty.SetInterpolationTypeToLinear()
    volumeProperty.ShadeOn()
    volumeProperty.SetAmbient(0.4)
    volumeProperty.SetDiffuse(0.6)
    volumeProperty.SetSpecular(0.2)

    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)

    ren.AddViewProp(volume)

     # Initialize the event loop and then start it.
    iren.Initialize()
    iren.Start()




def get_program_parameters():
    import argparse
    description = 'The skin extracted from a CT dataset of the head.'
    epilogue = '''
    Derived from VTK/Examples/Cxx/Medical1.cxx
    This example reads a volume dataset, extracts an isosurface that
     represents the skin and displays it.
    '''
    parser = argparse.ArgumentParser(description=description, epilog=epilogue,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('filename', help='FullHead.mhd.')
    args = parser.parse_args()
    return args.filename


if __name__ == '__main__':
    main()