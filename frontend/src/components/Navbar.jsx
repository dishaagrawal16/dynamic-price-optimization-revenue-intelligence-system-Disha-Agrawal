function Navbar({ title }) {
  return (
    <div className="h-16 bg-white shadow flex justify-between items-center px-8">

      <h2 className="text-2xl font-bold">
        {title}
      </h2>

      <div className="flex items-center gap-4">

        <button className="text-xl">🔔</button>

        <img
          src="https://i.pravatar.cc/40"
          alt="profile"
          className="rounded-full"
        />

        <span className="font-medium">
          Disha
        </span>

      </div>

    </div>
  );
}

export default Navbar;