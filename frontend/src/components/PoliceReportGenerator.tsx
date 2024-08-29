import React, { useState, useEffect, useRef, ChangeEvent, lazy, Suspense } from 'react';
import { Button } from './ui/button';
import { uploadAudio, generateReport } from '../api/apiService';
import { Spinner } from './ui/spinner';

const ReactMarkdown = lazy(() => import('react-markdown'));

const PoliceReportGenerator: React.FC = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcription, setTranscription] = useState("");
  const [report, setReport] = useState("");
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isTranscribing, setIsTranscribing] = useState(false);
  const [isGeneratingReport, setIsGeneratingReport] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const websocketRef = useRef<WebSocket | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const retryTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const failedChunkRef = useRef<Blob | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

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
                const retryChunk = new Blob(
                  failedChunkRef.current ? [failedChunkRef.current, ...chunksRef.current] : chunksRef.current,
                  { type: "audio/webm" }
                );
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

      mediaRecorderRef.current.ondataavailable = async (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
          if (websocketRef.current?.readyState === WebSocket.OPEN && !failedChunkRef.current) {
            const chunk = new Blob([event.data], { type: "audio/webm" });
            const arrayBuffer = await chunk.arrayBuffer();
            websocketRef.current.send(arrayBuffer);
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

      mediaRecorderRef.current.start(1000); // Send audio data every 1000ms (1 second)
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
    if (transcription) {
      setIsLoading(true);
      setError(null);
      setIsGeneratingReport(true);
      try {
        const result = await generateReport(transcription, "General Occurrence");
        setReport(result.report);
      } catch (error) {
        console.error("Report generation error:", error);
        setError("Failed to generate report. Please try again.");
      } finally {
        setIsLoading(false);
        setIsGeneratingReport(false);
      }
    }
  };

  const handleFileUpload = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setAudioBlob(file);
      setTranscription(""); // Clear any existing transcription
      setReport(""); // Clear any existing report
      setIsLoading(true);
      setIsTranscribing(true);
      setError(null);
      try {
        const result = await uploadAudio(file);
        setTranscription(result.text);
      } catch (error) {
        console.error("Upload error:", error);
        setError("Failed to upload and transcribe audio. Please try again.");
      } finally {
        setIsLoading(false);
        setIsTranscribing(false);
      }
    }
  };

  const triggerFileUpload = () => {
    fileInputRef.current?.click();
  };

  const getGenerateButtonText = () => {
    if (isLoading) return 'Processing...';
    if (isGeneratingReport) return 'Generating Report...';
    return 'Generate Report';
  };

  return (
    <div className="space-y-4 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <h2 className="text-2xl sm:text-3xl font-bold mb-4">Police Report Generator</h2>
      <p className="mb-4 text-sm sm:text-base">
        Record your report or upload an audio file, and let the AI handle the transcription and formatting.
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
          onClick={triggerFileUpload}
          disabled={isLoading}
          className="bg-gray-600 hover:bg-gray-700 text-white w-full sm:w-auto"
        >
          Upload Audio File
        </Button>
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileUpload}
          accept="audio/*"
          className="hidden"
        />
        <Button
          onClick={handleGenerateReport}
          disabled={!transcription || isLoading}
          className="bg-white hover:bg-gray-100 text-black w-full sm:w-auto"
        >
          {getGenerateButtonText()}
        </Button>
      </div>
      {isRecording && (
        <div className="mt-4 flex items-center">
          <div className="w-4 h-4 bg-red-500 rounded-full mr-2 animate-pulse"></div>
          <span>Recording...</span>
        </div>
      )}
      {audioBlob && !isRecording && (
        <div className="mt-4">
          <span>Audio file ready for processing</span>
        </div>
      )}
      {error && (
        <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}
      <div className="bg-gray-800 p-4 rounded-lg mt-6 relative">
        <h3 className="text-xl sm:text-2xl font-semibold mb-2 text-white">Transcription</h3>
        <div className="bg-gray-700 p-4 rounded-lg min-h-[200px] sm:min-h-[300px] max-h-[400px] sm:max-h-[500px] overflow-y-auto relative">
          {isTranscribing && (
            <div className="absolute inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center">
              <Spinner className="w-8 h-8 text-blue-500" />
            </div>
          )}
          {transcription ? (
            <p className="text-gray-200 whitespace-pre-wrap">{transcription}</p>
          ) : (
            <p className="text-gray-400 italic">
              Transcription will appear here...
            </p>
          )}
        </div>
      </div>
      <div className="bg-gray-800 p-4 rounded-lg mt-6 relative">
        <div className="flex justify-between items-center mb-2">
          <h3 className="text-xl sm:text-2xl font-semibold text-white">Generated Report</h3>
          <Button 
            className="bg-blue-500 hover:bg-blue-600 text-white"
            disabled={!report}
            onClick={() => setIsEditing(!isEditing)}
          >
            {isEditing ? 'Done' : 'Edit'}
          </Button>
        </div>
        <div className="bg-gray-700 p-4 rounded-lg min-h-[200px] sm:min-h-[300px] max-h-[400px] sm:max-h-[500px] overflow-y-auto relative">
          {isGeneratingReport && (
            <div className="absolute inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center">
              <Spinner className="w-8 h-8 text-blue-500" />
            </div>
          )}
          {report ? (
            isEditing ? (
              <textarea
                value={report}
                onChange={(e) => setReport(e.target.value)}
                className="w-full h-full bg-gray-800 text-gray-200 border-none resize-none focus:ring-0 p-2"
              />
            ) : (
              <Suspense fallback={<div>Loading...</div>}>
                <ReactMarkdown className="text-gray-200 prose prose-invert max-w-none">
                  {report}
                </ReactMarkdown>
              </Suspense>
            )
          ) : (
            <p className="text-gray-400 italic">
              Generated report will appear here...
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default PoliceReportGenerator;
