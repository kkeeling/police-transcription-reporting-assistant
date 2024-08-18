import axiosInstance from './axiosConfig';

export const sendAudioToBackend = async (audioBlob: Blob): Promise<string> => {
  // Simulate sending audio to backend
  await new Promise(resolve => setTimeout(resolve, 1000));
  return 'Audio received successfully';
};

export const getTranscriptionFromBackend = async (): Promise<string> => {
  // Simulate getting transcription from backend
  await new Promise(resolve => setTimeout(resolve, 2000));
  return 'This is a mock transcription of the audio file.';
};

// Placeholder for actual API call
export const transcribeAudio = async (audioBlob: Blob): Promise<string> => {
  try {
    await sendAudioToBackend(audioBlob);
    const transcription = await getTranscriptionFromBackend();
    return transcription;
  } catch (error) {
    console.error('Error in transcribeAudio:', error);
    throw error;
  }
};
