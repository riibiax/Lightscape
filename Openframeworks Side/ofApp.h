#pragma once

#include "ofMain.h"
#include "ofxiOS.h"
#include "ofxiOSExtras.h"
#include "ofxXmlSettings.h"
#include "ofxNetwork.h"

class ofApp : public ofxiOSApp{
	
    public:
        void setup();
        void update();
        void draw();
        void exit();
	
        void touchDown(ofTouchEventArgs & touch);
        void touchMoved(ofTouchEventArgs & touch);
        void touchUp(ofTouchEventArgs & touch);
        void touchDoubleTap(ofTouchEventArgs & touch);
        void touchCancelled(ofTouchEventArgs & touch);

        void lostFocus();
        void gotFocus();
        void gotMemoryWarning();
        void deviceOrientationChanged(int newOrientation);
    
        void setWoeid();
    
        ofxiOSCoreLocation * coreLocation;
    
        bool hasGPS;
    
        float lon, lat;
    
        ofHttpResponse resp;
    
        int woeid;
    
        ofTrueTypeFont text;
        string msg;
    
        //upload part
        void uploadDATA();
        ofxTCPClient tcpClient;
        string msgTx, msgRx;
        int connectTime;
        int deltaTime;
        bool weConnected;
        string ip;
        int port;
};


