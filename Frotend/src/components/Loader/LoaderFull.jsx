import { Loader2 } from "lucide-react";
import React from "react";

const LoaderFull = () => {
  return (
    <div className="flex items-center justify-center w-screen h-screen">
      <Loader2 className="text-gray-500 size-7 animate-spin" />
    </div>
  );
};

export default LoaderFull;
