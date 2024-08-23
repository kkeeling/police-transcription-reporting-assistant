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

export const uploadAudio = async (audioFile: File): Promise<{ text: string }> => {
  // Create a FormData object to send the file
  const formData = new FormData();
  formData.append('file', audioFile);

  // Simulate API call delay
  await new Promise(resolve => setTimeout(resolve, 2000));

  // Mock API response
  return { text: "This is a mock transcription of the uploaded audio file." };

  // Uncomment the following lines when you're ready to make actual API calls
  // const response = await fetch('http://localhost:8000/api/v1/upload-audio', {
  //   method: 'POST',
  //   body: formData,
  // });
  // if (!response.ok) {
  //   throw new Error('Failed to upload audio');
  // }
  // return response.json();
};
