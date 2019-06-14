'''
A simple Program for grabing video from basler camera and converting it to opencv img.

'''

from pypylon import pylon
import cv2
import time

# conecting to the first available camera
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

#set the dimentions og the image to grab
camera.Open()
# camera.Width.Value = 2592  # max width of Basler puA2500-14uc camera
# camera.Height.Value = 1944 # max height of Basler puA2500-14uc camera
# 100% beeld leert soms bandbreedte probleem op in VMWare????
camera.Width.Value = 2074  # 0.8% max width of Basler puA2500-14uc camera
camera.Height.Value = 1554 # 0.8% max height of Basler puA2500-14uc camera
camera.OffsetX.Value = 518
# camera.AcquisitionFrameRate.SetValue(14)

# set features of camera
camera.ExposureTime.Value = 20000
camera.ExposureAuto.SetValue('Off')
camera.BalanceWhiteAuto.SetValue('Off')
camera.LightSourcePreset.SetValue('Tungsten2800K')
camera.GainAuto.SetValue('Off')
# pylon.FeaturePersistence.Save("test.txt", camera.GetNodeMap())

print("Using device: ", camera.GetDeviceInfo().GetModelName())
print("width set: ",camera.Width.Value)
print("Height set: ",camera.Height.Value)

# The parameter MaxNumBuffer can be used to control the count of buffers
# allocated for grabbing. The default value of this parameter is 10.
camera.MaxNumBuffer = 5

# Grabing Continusely (video) with minimal delay
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
converter = pylon.ImageFormatConverter()

# converting to opencv bgr format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Access the image data
        image = converter.Convert(grabResult)
        img = image.GetArray()

        # do some image processing
        # img = cv2.GaussianBlur(img, (65,65), 0)

        # open the image in a window
        imS = cv2.resize(img, ((int)(camera.Width.Value/3)+1,
                               (int)(camera.Height.Value/3)+1))
        cv2.namedWindow('camera', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('camera', imS)

        # press esc (ascii 27) to exit
        k = cv2.waitKey(1)
        if k == 27:
            break
    grabResult.Release()

# Releasing the resource
camera.StopGrabbing()
cv2.destroyAllWindows()
