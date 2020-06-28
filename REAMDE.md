Metricscollector
sudo apt-get install iotedge=1.0.9.3-1 libiothsm-std=1.0.9.3-1

https://<iothubName>.azure-devices.net/twins/<deviceId>/modules/<moduleName>/methods?api-version=2018-06
'https://mythicaledge1.azure-devices.net/macbook/modules/PySendModule/methods?api-version=2020-03-13'
'SharedAccessSignature sr=mythicaledge1.azure-devices.net&sig=63f3dQcyGGEBH%2BmsIVEB/UbGs8IsGjEA1%2BHCq72fXGI%3D&se=1593318521&skn=iothubowner'
curl -X POST \
  https://<iothubName>.azure-devices.net/twins/<deviceId>/methods?api-version=2018-06-30 \
  -H 'Authorization: SharedAccessSignature sr=iothubname.azure-devices.net&sig=x&se=x&skn=iothubowner' \
  -H 'Content-Type: application/json' \
  -d '{
    "methodName": "reboot",
    "responseTimeoutInSeconds": 200,
    "payload": {
        "input1": "someInput",
        "input2": "anotherInput"
    }
}'

curl -X POST \
  https://mythicaledge1.azure-devices.net/twins/macbook/modules/PySendModule/methods?api-version=2020-03-13 \
  -H 'Authorization: SharedAccessSignature sr=mythicaledge1.azure-devices.net&sig=63f3dQcyGGEBH%2BmsIVEB/UbGs8IsGjEA1%2BHCq72fXGI%3D&se=1593318521&skn=iothubowner' \
  -H 'Content-Type: application/json' \
  -d '{ 
    "methodName": "method1", 
    "responseTimeoutInSeconds": 200, 
    "payload": { 
        "input1": "someInput", 
        "input2": "anotherInput" 
    } 
}'

az iot hub generate-sas-token -n mythicaledge1

'{"Message":"{\\"errorCode\\":400004,\\"trackingId\\":\\"de6939fbc5dc479da7f27a059e1f4188-G:0-TimeStamp:06/28/2020 02:41:51\\",\\"message\\":\\"methodName is null or empty.\\",\\"timestampUtc\\":\\"2020-06-28T02:41:51.9625624Z\\"}","ExceptionMessage":""}'