import { Plus } from "lucide-react";

const CreateCompanyButton = () => {
  return (
    <button className="flex items-center gap-2 px-4 py-2 text-white transition bg-blue-600 rounded-xl hover:bg-blue-700">
      <Plus size={18} />
      Create Company
    </button>
  );
};

export default CreateCompanyButton;
