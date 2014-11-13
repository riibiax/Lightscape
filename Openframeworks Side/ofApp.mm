#include "ofApp.h"

//--------------------------------------------------------------
void ofApp::setup(){	
	ofSetOrientation(OF_ORIENTATION_90_RIGHT);//Set iOS to Orientation Landscape Right
    ofEnableAlphaBlending();
    ofBackground(0,0,0);
	ofSetFrameRate(60);
    
    //no sleep mode
    [[UIApplication sharedApplication] setIdleTimerDisabled:YES];
    
    coreLocation = new ofxiOSCoreLocation();
	hasGPS = coreLocation->startLocation();
	
    woeid = 15015370;
    
    text.loadFont("fonts/Roboto-Regular.ttf", 32);
    text.setLetterSpacing(1.5);
    msg="";
    
    //uploadDATA
    // we don't want to be running to fast
	ofSetVerticalSync(true);
	//our send and recieve strings
	msgTx= "1\n";
	msgRx= "1\n";
	//are we connected to the server - if this fails we
	//will check every few seconds to see if the server exists
    ip="172.20.10.12";
    port=8888;
	weConnected = tcpClient.setup(ip, port);
	//optionally set the delimiter to something else.  The delimter in the client and the server have to be the same
	tcpClient.setMessageDelimiter("\n");
	connectTime = 0;
	deltaTime = 3700000;

}

//--------------------------------------------------------------
void ofApp::update(){

    if( deltaTime > 3600000 ){
        if(hasGPS){
            //cout<<coreLocation->getLatitude()<<" | "<< coreLocation->getLatitude() <<endl;
            lat=coreLocation->getLatitude();
            lon=coreLocation->getLongitude();
            setWoeid();
        }
        
        if(!weConnected)
            weConnected = tcpClient.setup(ip, port);

        msgTx = ofToString(lat)+","+ofToString(lon)+","+ofToString(woeid)+"\n";
        uploadDATA();
        connectTime = ofGetElapsedTimeMillis();
    }
    
    //if we are not connected lets try and reconnect every 1 hour
    deltaTime = ofGetElapsedTimeMillis() - connectTime;
}

//--------------------------------------------------------------
void ofApp::draw(){
    ofBackground(0, 0, 0);
    //Titre
    ofSetColor(0,0,0, 240);
    msg = "Thank you";
    text.drawString(msg, (ofGetWidth()-text.stringWidth(msg))/2, ofGetHeight()/2);
}

//--------------------------------------------------------------
void ofApp::uploadDATA(){
    if(tcpClient.send(msgTx)){
        //if data has been sent lets update our text
        string str = tcpClient.receive();
        if( str.length() > 0 ){
            msgRx = str;
        }
    }else if(!tcpClient.isConnected())
        weConnected = false;
}

//--------------------------------------------------------------
void ofApp::setWoeid(){
    char url[1024];
    sprintf(url, "http://query.yahooapis.com/v1/public/yql?q=select woeid from geo.placefinder where text=\"%f,%f\" and gflags=\"R\"", lat, lon);
    string urlString = url;
    for (size_t pos = urlString.find(' '); pos != string::npos; pos = urlString.find(' ', pos)){
        urlString.replace(pos, 1, "%20");
    }
    ofHttpResponse resp = ofLoadURL(urlString);
    ofxXmlSettings xmlBuffer;
    ofBuffer buffer = resp.data;
    xmlBuffer.loadFromBuffer(buffer.getText());
    woeid = ofToInt(xmlBuffer.getValue("query:results:Result:woeid", "0"));
}

//--------------------------------------------------------------
void ofApp::exit(){

}

//--------------------------------------------------------------
void ofApp::touchDown(ofTouchEventArgs & touch){
}

//--------------------------------------------------------------
void ofApp::touchMoved(ofTouchEventArgs & touch){

}

//--------------------------------------------------------------
void ofApp::touchUp(ofTouchEventArgs & touch){
    
}

//--------------------------------------------------------------
void ofApp::touchDoubleTap(ofTouchEventArgs & touch){

}

//--------------------------------------------------------------
void ofApp::touchCancelled(ofTouchEventArgs & touch){
    
}

//--------------------------------------------------------------
void ofApp::lostFocus(){

}

//--------------------------------------------------------------
void ofApp::gotFocus(){

}

//--------------------------------------------------------------
void ofApp::gotMemoryWarning(){

}

//--------------------------------------------------------------
void ofApp::deviceOrientationChanged(int newOrientation){

}

