import { useMemo, useState } from "react";
import { Search } from "lucide-react";
import SearchDropdown from "./SearchDropdown";
import { companies } from "./data";

const SearchBar = () => {
  const [query, setQuery] = useState("");
  const [show, setShow] = useState(false);

  const filtered = useMemo(() => {
    return companies.filter((company) =>
      company.name.toLowerCase().includes(query.toLowerCase()),
    );
  }, [query]);

  return (
    <div className="relative w-[430px]">
      <Search
        size={18}
        className="absolute -translate-y-1/2 left-4 top-1/2 text-slate-400"
      />

      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onFocus={() => setShow(true)}
        onBlur={() => setTimeout(() => setShow(false), 150)}
        placeholder="Search company..."
        className="w-full rounded-xl border bg-slate-50 py-2.5 pl-11 pr-4 outline-none focus:border-blue-500 focus:bg-white"
      />

      {show && query && <SearchDropdown companies={filtered} />}
    </div>
  );
};

export default SearchBar;
