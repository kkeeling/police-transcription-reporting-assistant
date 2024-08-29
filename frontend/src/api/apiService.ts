import axiosInstance from './axiosConfig';

export const uploadAudio = async (audioFile: File): Promise<{ text: string }> => {
  const formData = new FormData();
  formData.append('file', audioFile);

  try {
    const response = await axiosInstance.post('/api/v1/upload-audio', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
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

export const generateReport = async (transcription: string, reportType: string): Promise<{ report: string }> => {
  try {
    const response = await axiosInstance.post('/api/v1/generate_report', {
      transcription,
      report_type: reportType
    });

    if (response.status !== 200) {
      throw new Error('Failed to generate report');
    }

    return response.data;
  } catch (error) {
    console.error('Error generating report:', error);
    throw error;
  }
};
