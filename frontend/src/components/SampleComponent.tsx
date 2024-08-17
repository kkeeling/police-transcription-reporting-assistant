import React from 'react';
import { Button } from "@/components/ui/button";

const SampleComponent: React.FC = () => {
  return (
    <div className="p-4 bg-gray-100 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">Sample Component</h2>
      <p className="mb-4">This is a sample component using Tailwind CSS and shadcn/ui.</p>
      <Button>Click me!</Button>
    </div>
  );
};

export default SampleComponent;
