import React, { useState, useRef } from 'react'
import { Button } from "./ui/button"

const PoliceReportGenerator: React.FC = () => {
  const [isRecording, setIsRecording] = useState(false)
  const [transcription, setTranscription] = useState('')
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [playbackProgress, setPlaybackProgress] = useState(0)
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const chunksRef = useRef<Blob[]>([])
  const audioRef = useRef<HTMLAudioElement | null>(null)

  const handleStartRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      mediaRecorderRef.current = new MediaRecorder(stream)
      
      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data)
        }
      }

      mediaRecorderRef.current.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' })
        setAudioBlob(blob)
        chunksRef.current = []
      }

      mediaRecorderRef.current.start()
      setIsRecording(true)
    } catch (error) {
      console.error('Error starting recording:', error)
    }
  }

  const handleEndRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
    }
  }

  const handlePlay = () => {
    if (audioBlob) {
      if (!audioRef.current) {
        audioRef.current = new Audio(URL.createObjectURL(audioBlob))
        audioRef.current.addEventListener('ended', () => {
          setIsPlaying(false)
          setPlaybackProgress(0)
        })
        audioRef.current.addEventListener('timeupdate', () => {
          const progress = (audioRef.current!.currentTime / audioRef.current!.duration) * 100
          setPlaybackProgress(progress)
        })
      }

      if (isPlaying) {
        audioRef.current.pause()
        setIsPlaying(false)
      } else {
        audioRef.current.play()
        setIsPlaying(true)
      }
    }
  }

  const handleUploadAudio = () => {
    // Implement upload audio logic here
  }

  const handleGenerateReport = () => {
    // Implement report generation logic here
  }

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold mb-4">Police Report Generator</h2>
      <p className="mb-4">Upload an audio file or dictate your report and let the AI handle the formatting.</p>
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
          {isPlaying ? 'Pause' : 'Play'}
        </Button>
        <Button 
          onClick={handleUploadAudio}
          className="bg-white hover:bg-gray-100 text-black"
        >
          Upload Audio
        </Button>
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
      <div className="bg-gray-800 p-4 rounded-lg min-h-[200px] mt-6">
        <p className="text-gray-400">{transcription || 'Transcription will appear here...'}</p>
      </div>
      <Button 
        onClick={handleGenerateReport}
        className="bg-white hover:bg-gray-100 text-black"
      >
        Generate Report
      </Button>
    </div>
  )
}

export default PoliceReportGenerator
