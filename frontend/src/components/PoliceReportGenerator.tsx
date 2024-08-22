import React, { useState, useEffect, useRef } from 'react';
import { Button } from "./ui/button";
import { transcribeAudio } from "../api/mockApiService";

const PoliceReportGenerator: React.FC = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcription, setTranscription] = useState("");
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const websocketRef = useRef<WebSocket | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const retryTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const failedChunkRef = useRef<Blob | null>(null);

  useEffect(() => {
    return () => {
      if (websocketRef.current) {
        websocketRef.current.close();
      }
      if (retryTimeoutRef.current) {
        clearTimeout(retryTimeoutRef.current);
      }
    };
  }, []);

  const startRecording = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);

      websocketRef.current = new WebSocket('ws://localhost:8000/api/v1/stream-audio');
      websocketRef.current.onopen = () => {
        setIsRecording(true);
        setIsLoading(false);
      };

      websocketRef.current.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.status === 'success') {
          setTranscription(prev => prev + ' ' + data.transcription);
          failedChunkRef.current = null; // Clear the failed chunk on success
        } else if (data.status === 'error') {
          if (data.detail === 'Rate limit exceeded' && data.retry_after) {
            const retryAfter = parseInt(data.retry_after, 10) * 1000; // Convert to milliseconds
            retryTimeoutRef.current = setTimeout(() => {
              if (websocketRef.current?.readyState === WebSocket.OPEN) {
                const retryChunk = new Blob([failedChunkRef.current, ...chunksRef.current], { type: "audio/webm" });
                websocketRef.current.send(retryChunk);
                chunksRef.current = []; // Clear chunks after sending
              }
            }, retryAfter);
          } else {
            setError(data.message);
          }
        }
      };

      websocketRef.current.onerror = (error) => {
        console.error('WebSocket error:', error);
        setError('WebSocket error occurred');
        setIsRecording(false);
        setIsLoading(false);
      };

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
          if (websocketRef.current?.readyState === WebSocket.OPEN && !failedChunkRef.current) {
            const chunk = new Blob([event.data], { type: "audio/webm" });
            websocketRef.current.send(chunk);
            failedChunkRef.current = chunk; // Store the last sent chunk
          }
        }
      };

      mediaRecorderRef.current.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: "audio/webm" });
        setAudioBlob(blob);
        chunksRef.current = [];
        failedChunkRef.current = null;
      };

      mediaRecorderRef.current.start(250); // Send audio data every 250ms
    } catch (err) {
      console.error('Error starting recording:', err);
      setError('Failed to start recording');
      setIsLoading(false);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
    }
    if (websocketRef.current) {
      websocketRef.current.close();
    }
    if (retryTimeoutRef.current) {
      clearTimeout(retryTimeoutRef.current);
    }
    setIsRecording(false);
  };

  const handleGenerateReport = async () => {
    if (audioBlob) {
      setIsLoading(true);
      setError(null);
      try {
        const result = await transcribeAudio(audioBlob);
        setTranscription(result);
      } catch (error) {
        console.error("Transcription error:", error);
        setError("Failed to transcribe audio. Please try again.");
      } finally {
        setIsLoading(false);
      }
    }
  };

  return (
    <div className="space-y-4 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <h2 className="text-2xl sm:text-3xl font-bold mb-4">Police Report Generator</h2>
      <p className="mb-4 text-sm sm:text-base">
        Record your report and let the AI handle the transcription and formatting.
      </p>
      <div className="flex flex-col sm:flex-row flex-wrap gap-4">
        <Button
          onClick={isRecording ? stopRecording : startRecording}
          disabled={isLoading}
          className="bg-gray-600 hover:bg-gray-700 text-white w-full sm:w-auto"
        >
          {isLoading ? 'Preparing...' : isRecording ? 'Stop Recording' : 'Start Recording'}
        </Button>
        <Button
          onClick={handleGenerateReport}
          disabled={!audioBlob || isLoading}
          className="bg-white hover:bg-gray-100 text-black w-full sm:w-auto"
        >
          {isLoading ? "Transcribing..." : "Generate Report"}
        </Button>
      </div>
      {isRecording && (
        <div className="mt-4 flex items-center">
          <div className="w-4 h-4 bg-red-500 rounded-full mr-2 animate-pulse"></div>
          <span>Recording...</span>
        </div>
      )}
      {error && (
        <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}
      <div className="bg-gray-800 p-4 rounded-lg mt-6">
        <h3 className="text-xl sm:text-2xl font-semibold mb-2 text-white">Transcription</h3>
        <div className="bg-gray-700 p-4 rounded-lg min-h-[200px] sm:min-h-[300px] max-h-[400px] sm:max-h-[500px] overflow-y-auto">
          {transcription ? (
            <p className="text-gray-200 whitespace-pre-wrap">{transcription}</p>
          ) : (
            <p className="text-gray-400 italic">
              Transcription will appear here...
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default PoliceReportGenerator;
