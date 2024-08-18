import React, { useState, useRef, ChangeEvent } from "react";
import { Button } from "./ui/button";
import { transcribeAudio } from "../api/mockApiService";

const PoliceReportGenerator: React.FC = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcription, setTranscription] = useState("");
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [playbackProgress, setPlaybackProgress] = useState(0);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [recordingError, setRecordingError] = useState<string | null>(null);
  const [playbackError, setPlaybackError] = useState<string | null>(null);
  const [isTranscribing, setIsTranscribing] = useState(false);
  const [transcriptionError, setTranscriptionError] = useState<string | null>(
    null
  );
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleStartRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      mediaRecorderRef.current.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: "audio/webm" });
        setAudioBlob(blob);
        chunksRef.current = [];
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
      setRecordingError(null);
    } catch (error) {
      console.error("Error starting recording:", error);
      setRecordingError(
        "Failed to start recording. Please check your microphone permissions."
      );
    }
  };

  const handleEndRecording = async () => {
    if (mediaRecorderRef.current && isRecording) {
      try {
        mediaRecorderRef.current.stop();
        setIsRecording(false);
        setRecordingError(null);

        console.log("Recording stopped");
        // Wait for the 'onstop' event to fire and create the audioBlob
        await new Promise((resolve) => setTimeout(resolve, 100));

        console.log("Audio blob created");
        console.log(audioBlob);
        if (audioBlob) {
          setIsTranscribing(true);
          setTranscriptionError(null);
          try {
            const result = await transcribeAudio(audioBlob);
            setTranscription(result);
          } catch (error) {
            console.error("Transcription error:", error);
            setTranscriptionError(
              "Failed to transcribe audio. Please try again."
            );
          } finally {
            setIsTranscribing(false);
          }
        }
      } catch (error) {
        console.error("Error stopping recording:", error);
        setRecordingError("Failed to stop recording. Please try again.");
      }
    }
  };

  const handlePlay = () => {
    if (audioBlob) {
      if (!audioRef.current) {
        audioRef.current = new Audio(URL.createObjectURL(audioBlob));
        audioRef.current.addEventListener("ended", () => {
          setIsPlaying(false);
          setPlaybackProgress(0);
        });
        audioRef.current.addEventListener("timeupdate", () => {
          const progress =
            (audioRef.current!.currentTime / audioRef.current!.duration) * 100;
          setPlaybackProgress(progress);
        });
        audioRef.current.addEventListener("error", (e) => {
          console.error("Audio playback error:", e);
          setPlaybackError("Failed to play audio. Please try again.");
        });
      }

      try {
        if (isPlaying) {
          audioRef.current.pause();
          setIsPlaying(false);
        } else {
          audioRef.current.play();
          setIsPlaying(true);
        }
        setPlaybackError(null);
      } catch (error) {
        console.error("Playback error:", error);
        setPlaybackError("Failed to play audio. Please try again.");
      }
    }
  };

  const handleUploadAudio = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleFileChange = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      if (file.type.startsWith("audio/")) {
        const reader = new FileReader();
        reader.onload = async (e) => {
          const blob = new Blob([e.target?.result as ArrayBuffer], {
            type: file.type,
          });
          setAudioBlob(blob);
          setUploadError(null);

          setIsTranscribing(true);
          setTranscriptionError(null);
          try {
            const result = await transcribeAudio(blob);
            setTranscription(result);
          } catch (error) {
            console.error("Transcription error:", error);
            setTranscriptionError(
              "Failed to transcribe audio. Please try again."
            );
          } finally {
            setIsTranscribing(false);
          }
        };
        reader.onerror = () => {
          setUploadError("Failed to read the audio file. Please try again.");
        };
        reader.readAsArrayBuffer(file);
      } else {
        setUploadError("Please upload a valid audio file.");
      }
    }
  };

  const handleGenerateReport = async () => {
    if (audioBlob) {
      setIsTranscribing(true);
      setTranscriptionError(null);
      try {
        const result = await transcribeAudio(audioBlob);
        setTranscription(result);
      } catch (error) {
        console.error("Transcription error:", error);
        setTranscriptionError("Failed to transcribe audio. Please try again.");
      } finally {
        setIsTranscribing(false);
      }
    }
  };

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold mb-4">Police Report Generator</h2>
      <p className="mb-4">
        Upload an audio file or dictate your report and let the AI handle the
        formatting.
      </p>
      <div className="flex flex-wrap gap-4">
        <Button
          onClick={handleStartRecording}
          disabled={isRecording}
          className="bg-gray-600 hover:bg-gray-700 text-white"
        >
          Start Recording
        </Button>
        <Button
          onClick={handleEndRecording}
          disabled={!isRecording}
          className="bg-gray-600 hover:bg-gray-700 text-white"
        >
          End Recording
        </Button>
        <Button
          onClick={handlePlay}
          disabled={!audioBlob}
          className="bg-gray-600 hover:bg-gray-700 text-white"
        >
          {isPlaying ? "Pause" : "Play"}
        </Button>
        <Button
          onClick={handleUploadAudio}
          className="bg-white hover:bg-gray-100 text-black"
        >
          Upload Audio
        </Button>
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          accept="audio/*"
          className="hidden"
        />
      </div>
      {isRecording && (
        <div className="mt-4 flex items-center">
          <div className="w-4 h-4 bg-red-500 rounded-full mr-2 animate-pulse"></div>
          <span>Recording...</span>
        </div>
      )}
      {audioBlob && (
        <div className="mt-4">
          <div className="bg-gray-200 h-2 rounded-full">
            <div
              className="bg-blue-500 h-2 rounded-full"
              style={{ width: `${playbackProgress}%` }}
            ></div>
          </div>
        </div>
      )}
      {(recordingError || uploadError || playbackError) && (
        <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
          {recordingError || uploadError || playbackError}
        </div>
      )}
      <div className="bg-gray-800 p-4 rounded-lg mt-6">
        <h3 className="text-xl font-semibold mb-2">Transcription</h3>
        <div className="bg-gray-700 p-4 rounded-lg min-h-[200px] max-h-[400px] overflow-y-auto">
          {transcription ? (
            <p className="text-gray-200 whitespace-pre-wrap">{transcription}</p>
          ) : (
            <p className="text-gray-400 italic">
              Transcription will appear here...
            </p>
          )}
        </div>
      </div>
      <Button
        onClick={handleGenerateReport}
        className="bg-white hover:bg-gray-100 text-black mt-4"
        disabled={!audioBlob || isTranscribing}
      >
        {isTranscribing ? "Transcribing..." : "Generate Report"}
      </Button>
      {transcriptionError && (
        <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
          {transcriptionError}
        </div>
      )}
    </div>
  );
};

export default PoliceReportGenerator;
