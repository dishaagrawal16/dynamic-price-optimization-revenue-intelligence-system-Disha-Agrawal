import Sidebar from "./Sidebar";
import Navbar from "./Navbar";

function Layout({ children, title }) {
  return (
    <div className="flex">
      <Sidebar />

      <div className="ml-64 flex-1 min-h-screen bg-gray-100">
        <Navbar title={title} />

        <div className="p-8">
          {children}
        </div>
      </div>
    </div>
  );
}

export default Layout;