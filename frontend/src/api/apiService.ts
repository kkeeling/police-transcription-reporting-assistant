import axiosInstance from './axiosConfig';

export const uploadAudio = async (audioFile: File): Promise<{ text: string }> => {
  const formData = new FormData();
  formData.append('file', audioFile);

  try {
    const response = await axiosInstance.post('/api/v1/upload-audio', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    if (response.status !== 200) {
      throw new Error('Failed to upload audio');
    }

    return response.data;
  } catch (error) {
    console.error('Error uploading audio:', error);
    throw error;
  }
};
