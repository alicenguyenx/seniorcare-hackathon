"use client";

import { useState, useRef } from "react";

export default function AGEentHome() {
  const [messages, setMessages] = useState([
    { role: "ai", text: "Hi there! I am AGEent. How can I help you navigate the government maze today?" }
  ]);
  const [inputText, setInputText] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [fontSize, setFontSize] = useState("text-xl"); 
  const [status, setStatus] = useState("Ready to assist you...");
  const [isLoading, setIsLoading] = useState(false);

  const mediaRecorder = useRef<MediaRecorder | null>(null);
  const audioChunks = useRef<Blob[]>([]);

  const [view, setView] = useState<"home" | "auth">("home");
  const [authMode, setAuthMode] = useState<"signin" | "signup">("signin");
  const [signupStep, setSignupStep] = useState<1 | 2>(1);

  const increaseFont = () => setFontSize("text-2xl md:text-3xl");
  const decreaseFont = () => setFontSize("text-lg md:text-xl");

  // Voice reading function
  const speakText = (text: string) => {
    window.speechSynthesis.cancel(); 
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "en-US";
    utterance.rate = 0.9; 
    utterance.pitch = 1;
    window.speechSynthesis.speak(utterance);
  };

  const toggleRecording = () => {
    if (!isRecording) {
      startRecording();
    } else {
      stopRecording();
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder.current = new MediaRecorder(stream);
      audioChunks.current = [];

      mediaRecorder.current.ondataavailable = (event) => {
        audioChunks.current.push(event.data);
      };

      mediaRecorder.current.onstop = async () => {
        // Instead of sending audio, run the demo scenario
        await handleDemoVoiceProcessing();
      };

      mediaRecorder.current.start();
      setIsRecording(true);
      setStatus("[STATUS] Listening to your voice...");
    } catch (err) {
      alert("Please allow microphone access to record the demo.");
    }
  };

  const stopRecording = () => {
    if (mediaRecorder.current) {
      mediaRecorder.current.stop();
      setIsRecording(false);
    }
  };

  // Voice processing (without backend)
  const handleDemoVoiceProcessing = async () => {
    setIsLoading(true);
    setStatus("[STATUS] Processing audio with Nova Sonic...");

    // Simulate 1.5 seconds for the AI to process
    await new Promise(resolve => setTimeout(resolve, 1500));

    // Demo user voice text
    const demoUserVoiceText = "I need help filling out my Medicare application. The paperwork is too confusing.";
    setMessages(prev => [...prev, { role: "user", text: demoUserVoiceText }]);
    setStatus("[STATUS] Analyzing request with Nova Lite...");

    // Simulate 1.5 seconds for the AI to process
    await new Promise(resolve => setTimeout(resolve, 1500));

    // Demo AI response
    const demoAiResponse = "I completely understand, those forms can be overwhelming. I have opened the Medicare portal for you. To get started, could you please tell me your Social Security Number?";
    
    setMessages(prev => [...prev, { role: "ai", text: demoAiResponse }]);
    setStatus("Ready to assist you...");
    setIsLoading(false);
    
    // Voice output
    speakText(demoAiResponse);
  };

  // Chat text processing (without backend)
  const handleSendMessage = async () => {
    if (!inputText.trim()) return;
    
    const userText = inputText;
    setMessages(prev => [...prev, { role: "user", text: userText }]);
    setInputText("");
    setStatus("[STATUS] Sending text to AI...");
    setIsLoading(true);

    // Simulate 1.5 seconds for the AI to process
    await new Promise(resolve => setTimeout(resolve, 1500));

    // Demo AI response
    const demoAiResponse = "Thank you. I have securely captured that information. I am now automatically filling out section A of your Medicare form using Nova Act. Please wait a moment...";
    
    setMessages(prev => [...prev, { role: "ai", text: demoAiResponse }]);
    setStatus("[STATUS] Nova Act is automating your form...");
    setIsLoading(false);
    
    speakText(demoAiResponse);
  };

  return (
    <main className="min-h-screen bg-amber-50 text-blue-950 p-6 md:p-12 flex flex-col items-center font-sans selection:bg-purple-200">
      
      {/* THANH ĐIỀU HƯỚNG */}
      <nav className="w-full max-w-5xl flex justify-end gap-4 mb-8 text-blue-950 font-bold text-lg md:text-xl border-b-2 border-slate-200 pb-4">
        <button onClick={() => setView("home")} className={`hover:text-purple-600 transition ${view === "home" ? "text-purple-700 underline underline-offset-8" : ""}`}>Home</button>
        <span className="text-slate-300">|</span>
        <button onClick={() => { setView("auth"); setAuthMode("signin"); }} className={`hover:text-purple-600 transition ${view === "auth" && authMode === "signin" ? "text-purple-700 underline underline-offset-8" : ""}`}>Login</button>
        <span className="text-slate-300">|</span>
        <button onClick={() => { setView("auth"); setAuthMode("signup"); setSignupStep(1); }} className={`hover:text-purple-600 transition ${view === "auth" && authMode === "signup" ? "text-purple-700 underline underline-offset-8" : ""}`}>Sign up</button>
      </nav>

      {/* GIAO DIỆN TRANG CHỦ (HOME) */}
      {view === "home" && (
        <div className="w-full flex flex-col items-center">
          {/* HEADER */}
          <header className="w-full max-w-5xl flex flex-col md:flex-row justify-between items-start md:items-center mb-12">
            <div className="mb-6 md:mb-0">
              <h1 className="text-5xl md:text-7xl font-black tracking-tight flex items-baseline">
                AGEent<span className="text-purple-400">.</span>
              </h1>
              <p className="text-purple-600 font-semibold mt-2 text-lg md:text-xl">
                Your personal agent for the government &apos;maze&apos;.
              </p>
            </div>
            <div className="flex gap-4">
              <button onClick={decreaseFont} className="w-14 h-14 bg-white border-2 border-blue-950 rounded-xl text-2xl font-bold hover:bg-slate-100 transition shadow-sm flex items-center justify-center">A-</button>
              <button onClick={increaseFont} className="w-14 h-14 bg-white border-2 border-blue-950 rounded-xl text-2xl font-bold hover:bg-slate-100 transition shadow-sm flex items-center justify-center">A+</button>
            </div>
          </header>

          {/* Image section */}
          <section className="w-full max-w-5xl grid md:grid-cols-2 gap-8 mb-16">
            <div className="bg-white p-8 rounded-3xl shadow-md border border-slate-200 flex flex-col items-center text-center transition hover:shadow-lg">
              <div className="w-full h-64 bg-slate-200 rounded-2xl mb-6 overflow-hidden flex items-center justify-center">
                <img src="old.png" alt="Confusing paper forms" className="w-full h-full object-cover" />
              </div>
              <p className="text-2xl font-bold text-blue-950">Tired of confusing paper forms?</p>
            </div>
            <div className="bg-white p-8 rounded-3xl shadow-md border border-slate-200 flex flex-col items-center text-center transition hover:shadow-lg">
              <div className="w-full h-64 bg-purple-100 rounded-2xl mb-6 overflow-hidden flex items-center justify-center">
                <img src="new.png" alt="Happy senior using AI" className="w-full h-full object-cover" />
              </div>
              <p className="text-2xl font-bold text-blue-950">Try AGEent! Just speak or text to our AI to complete your application.</p>
            </div>
          </section>

          {/* Detailed description */}
          <section className="w-full max-w-4xl text-center mb-16">
            <p className="text-xl md:text-2xl text-slate-700 leading-relaxed font-medium">
              AGEent uses agentic artificial intelligence to help seniors navigate the government maze, automate complex benefit applications, and beat the digital exclusion of outdated bureaucracy. Built with Nova Act and AWS, we transform cluttered portals into a single voice-command, ensuring the Medicare and Social Security benefits seniors earned are never more than a conversation away.
            </p>
          </section>

          {/* Chat & status area */}
          <section className="w-full max-w-4xl flex flex-col items-center mb-20">
            <h2 className="text-3xl md:text-4xl font-bold mb-8 text-center text-blue-950">Hi, how can I help you today?</h2>
            
            <div className="w-full bg-white rounded-3xl shadow-xl border border-slate-100 p-8 flex flex-col space-y-6">
              <div className="flex flex-col gap-4">
                {messages.map((msg, index) => (
                  <div key={index} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`${msg.role === 'user' ? 'bg-blue-900 text-white rounded-tr-none' : 'bg-slate-100 text-blue-950 rounded-tl-none'} p-6 rounded-3xl ${fontSize} font-semibold max-w-[85%] shadow-sm border border-slate-200`}>
                      {msg.text}
                    </div>
                  </div>
                ))}
                {isLoading && (
                  <div className="flex justify-start">
                    <div className={`bg-slate-100 text-slate-500 p-6 rounded-3xl rounded-tl-none ${fontSize} font-semibold max-w-[85%] shadow-sm border border-slate-200 animate-pulse`}>
                      Typing...
                    </div>
                  </div>
                )}
              </div>
              
              <div className="mt-6 p-5 bg-purple-50 border-l-4 border-purple-400 rounded-r-2xl">
                <p className="text-purple-700 font-bold text-xl animate-pulse tracking-wide">{status}</p>
              </div>
            </div>
          </section>

          {/* Bottom action area */}
          <section className="w-full max-w-3xl flex flex-col items-center gap-6 pb-24">
            <button
              onClick={toggleRecording}
              className={`flex items-center justify-center w-40 h-40 rounded-full shadow-2xl transition-all ${
                isRecording 
                  ? "bg-red-500 hover:bg-red-600 animate-pulse scale-110" 
                  : "bg-blue-950 hover:bg-blue-900 hover:scale-105"
              }`}
            >
              {isRecording ? (
                <svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 24 24" fill="white" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg>
              ) : (
                <svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/></svg>
              )}
            </button>
            <h3 className="text-3xl font-black tracking-widest text-blue-950 uppercase">{isRecording ? "Listening..." : "Tap to Speak"}</h3>

            <div className="w-full flex gap-4 mt-8">
              <input
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                placeholder="Or type your question here..."
                disabled={isLoading}
                className="flex-1 p-6 text-xl bg-white border-2 border-slate-300 rounded-2xl focus:outline-none focus:border-blue-950 shadow-sm transition disabled:bg-slate-100 disabled:text-slate-400"
              />
              <button 
                onClick={handleSendMessage}
                disabled={isLoading}
                className="p-6 bg-blue-950 hover:bg-blue-900 text-white rounded-2xl transition-colors shadow-lg flex items-center justify-center disabled:bg-slate-400"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></svg>
              </button>
            </div>
          </section>
        </div>
      )}

      {/* Auth interface */}
      {view === "auth" && (
        <div className="w-full max-w-xl bg-white rounded-3xl shadow-2xl border border-slate-200 p-8 md:p-12 mt-4">
          <div className="flex bg-slate-100 rounded-full p-2 mb-10">
            <button onClick={() => { setAuthMode("signin"); setSignupStep(1); }} className={`flex-1 py-3 rounded-full text-xl font-bold transition-all ${authMode === "signin" ? "bg-white text-blue-700 shadow border-2 border-blue-700" : "text-slate-500 hover:text-slate-800"}`}>Sign in</button>
            <button onClick={() => { setAuthMode("signup"); setSignupStep(1); }} className={`flex-1 py-3 rounded-full text-xl font-bold transition-all ${authMode === "signup" ? "bg-white text-blue-700 shadow border-2 border-blue-700" : "text-slate-500 hover:text-slate-800"}`}>Create an account</button>
          </div>

          {authMode === "signin" && (
            <div className="flex flex-col gap-6">
              <h2 className="text-4xl font-black text-slate-800 mb-4">Sign in for existing users</h2>
              <div className="flex flex-col gap-2">
                <label className="text-xl font-bold text-slate-800">Email address</label>
                <input type="email" className="p-4 border border-slate-300 rounded-xl text-lg focus:outline-none focus:border-blue-700 focus:ring-1 focus:ring-blue-700" />
              </div>
              <div className="flex flex-col gap-2">
                <label className="text-xl font-bold text-slate-800">Password</label>
                <input type="password" className="p-4 border border-slate-300 rounded-xl text-lg focus:outline-none focus:border-blue-700 focus:ring-1 focus:ring-blue-700" />
              </div>
              <div className="flex items-center gap-3">
                <input type="checkbox" id="show-pwd" className="w-5 h-5 accent-blue-700" />
                <label htmlFor="show-pwd" className="text-lg text-slate-700">Show password</label>
              </div>
              <button className="w-full bg-[#2A62A9] hover:bg-blue-800 text-white font-bold text-2xl py-5 rounded-xl mt-6 transition-colors shadow-md">Submit</button>
            </div>
          )}

          {authMode === "signup" && signupStep === 1 && (
            <div className="flex flex-col gap-6">
              <h2 className="text-4xl font-black text-slate-800 mb-2">Create an account</h2>
              <div className="flex flex-col gap-2">
                <label className="text-xl font-bold text-slate-800">Name</label>
                <input type="text" className="p-4 border border-slate-300 rounded-xl text-lg focus:outline-none focus:border-blue-700 focus:ring-1 focus:ring-blue-700" />
              </div>
              <div className="flex flex-col gap-2">
                <label className="text-xl font-bold text-slate-800">Address</label>
                <input type="text" className="p-4 border border-slate-300 rounded-xl text-lg focus:outline-none focus:border-blue-700 focus:ring-1 focus:ring-blue-700" />
              </div>
              <div className="flex flex-col gap-2">
                <label className="text-xl font-bold text-slate-800">Email address</label>
                <input type="email" className="p-4 border border-slate-300 rounded-xl text-lg focus:outline-none focus:border-blue-700 focus:ring-1 focus:ring-blue-700" />
              </div>
              <div className="flex flex-col gap-2">
                <label className="text-xl font-bold text-slate-800">Secure password</label>
                <input type="password" className="p-4 border border-slate-300 rounded-xl text-lg focus:outline-none focus:border-blue-700 focus:ring-1 focus:ring-blue-700" />
                <p className="text-base text-slate-600 font-medium mt-1">Passwords must be at least 12 characters and should not include commonly used words or phrases.</p>
              </div>
              <button onClick={() => setSignupStep(2)} className="w-full bg-[#2A62A9] hover:bg-blue-800 text-white font-bold text-2xl py-5 rounded-xl mt-6 transition-colors shadow-md">Continue</button>
            </div>
          )}

          {authMode === "signup" && signupStep === 2 && (
            <div className="flex flex-col gap-6">
              <h2 className="text-3xl font-black text-slate-800 mb-2">Authentication methods</h2>
              <p className="text-lg text-slate-600 font-medium">Select one or more authentication methods to secure your account:</p>
              <div className="flex flex-col gap-3 mt-2">
                <h3 className="text-lg font-black text-green-700 uppercase tracking-wider">More secure</h3>
                <label className="flex items-center gap-4 p-4 border-2 border-slate-200 rounded-xl cursor-pointer hover:border-blue-700 hover:bg-slate-50 transition-all"><input type="checkbox" className="w-6 h-6 accent-blue-700 rounded" /><span className="text-xl font-bold text-slate-800">Face or touch unlock</span></label>
                <label className="flex items-center gap-4 p-4 border-2 border-slate-200 rounded-xl cursor-pointer hover:border-blue-700 hover:bg-slate-50 transition-all"><input type="checkbox" className="w-6 h-6 accent-blue-700 rounded" /><span className="text-xl font-bold text-slate-800">Security key</span></label>
                <label className="flex items-center gap-4 p-4 border-2 border-slate-200 rounded-xl cursor-pointer hover:border-blue-700 hover:bg-slate-50 transition-all"><input type="checkbox" className="w-6 h-6 accent-blue-700 rounded" /><span className="text-xl font-bold text-slate-800">Government/Military ID (PIV/CAC)</span></label>
              </div>
              <div className="flex flex-col gap-3 mt-4">
                <h3 className="text-lg font-black text-orange-600 uppercase tracking-wider">Less secure</h3>
                <label className="flex items-center gap-4 p-4 border-2 border-slate-200 rounded-xl cursor-pointer hover:border-blue-700 hover:bg-slate-50 transition-all"><input type="checkbox" className="w-6 h-6 accent-blue-700 rounded" /><span className="text-xl font-bold text-slate-800">Authentication application</span></label>
                <label className="flex items-center gap-4 p-4 border-2 border-slate-200 rounded-xl cursor-pointer hover:border-blue-700 hover:bg-slate-50 transition-all"><input type="checkbox" className="w-6 h-6 accent-blue-700 rounded" /><span className="text-xl font-bold text-slate-800">Text/voice message</span></label>
                <label className="flex items-center gap-4 p-4 border-2 border-slate-200 rounded-xl cursor-pointer hover:border-blue-700 hover:bg-slate-50 transition-all"><input type="checkbox" className="w-6 h-6 accent-blue-700 rounded" /><span className="text-xl font-bold text-slate-800">Backup codes</span></label>
              </div>
              <div className="flex gap-4 mt-6">
                <button onClick={() => setSignupStep(1)} className="w-1/3 bg-slate-200 hover:bg-slate-300 text-slate-800 font-bold text-xl py-5 rounded-xl transition-colors shadow-sm">Back</button>
                <button onClick={() => { setView("home"); setSignupStep(1); alert("Account created successfully!"); }} className="w-2/3 bg-[#2A62A9] hover:bg-blue-800 text-white font-bold text-xl py-5 rounded-xl transition-colors shadow-md">Finish</button>
              </div>
            </div>
          )}
        </div>
      )}
    </main>
  );
}

