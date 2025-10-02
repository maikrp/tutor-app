import { useEffect, useState } from "react";
import { supabase } from "./supabase";

export default function App() {
  const [pendientes, setPendientes] = useState([]);
  const [realizados, setRealizados] = useState([]);

  useEffect(() => {
    fetchAjustes();
  }, []);

  async function fetchAjustes() {
    const { data: pend } = await supabase
      .from("ajustes")
      .select("*")
      .eq("realizado", false)
      .order("fecha_hora", { ascending: true });

    const { data: real } = await supabase
      .from("ajustes")
      .select("*")
      .eq("realizado", true)
      .order("fecha_hora", { ascending: true });

    setPendientes(pend || []);
    setRealizados(real || []);
  }

  async function marcarRealizado(id) {
    await supabase.from("ajustes").update({ realizado: true }).eq("id", id);
    fetchAjustes();
  }

  return (
    <div className="h-screen bg-gray-100 flex items-center justify-center">
      {/* Recuadro adaptativo */}
      <div className="w-full h-full md:max-w-md md:h-auto bg-white rounded-none md:rounded-3xl shadow-none md:shadow-xl overflow-hidden border-0 md:border border-gray-200 flex flex-col">
        
        {/* Header fijo arriba */}
        <header className="bg-indigo-700 text-white py-4 shadow flex items-center justify-between px-4">
          <img
            src="/logo.jpg"
            alt="Logo INS"
            className="w-10 h-10 rounded-full shadow-md object-contain"
          />
          <h1 className="text-lg font-bold">Control de Ajustes</h1>
          <div className="flex flex-col items-center">
            <img
              src="/medicas.png"
              alt="Médicas"
              className="w-8 h-8 object-contain"
            />
            <span className="text-[10px]">Médicas</span>
          </div>
        </header>

        {/* Contenido scrollable en móvil */}
        <main className="flex-1 overflow-y-auto p-4 space-y-8">
          
          {/* Pendientes */}
          <section>
            <h2 className="text-lg font-semibold text-gray-700 mb-3">Pendientes</h2>
            {pendientes.length === 0 ? (
              <p className="text-gray-500 text-center">✅ No hay ajustes pendientes</p>
            ) : (
              <div className="space-y-4">
                {pendientes.map((a) => (
                  <div
                    key={a.id}
                    className="p-4 rounded-2xl border border-gray-200 shadow-sm bg-gray-50"
                  >
                    <p className="font-semibold text-gray-700">
                      {new Date(a.fecha_hora).toLocaleString()}
                    </p>
                    <p className="mt-2 text-gray-600">
                      🔴 {a.red} | 🟠 {a.orange} | 🟡 {a.yellow} | 🟢 {a.green} | 🔵 {a.blue} | 🟣 {a.purple}
                    </p>
                    <button
                      onClick={() => marcarRealizado(a.id)}
                      className="mt-3 w-full py-3 rounded-lg bg-gradient-to-r from-green-500 to-blue-500 text-white font-semibold shadow hover:opacity-90 transition"
                    >
                      Confirmar realizado
                    </button>
                  </div>
                ))}
              </div>
            )}
          </section>

          {/* Historial */}
          <section className="pt-6 border-t border-gray-200">
            <h2 className="text-lg font-semibold text-gray-700 mb-3">Historial</h2>
            {realizados.length === 0 ? (
              <p className="text-gray-500 text-center">No hay ajustes confirmados aún</p>
            ) : (
              <ul className="space-y-2">
                {realizados.map((a) => (
                  <li
                    key={a.id}
                    className="p-3 rounded-xl border border-gray-200 flex items-center justify-between shadow-sm bg-gray-50"
                  >
                    <span className="text-gray-700">
                      {new Date(a.fecha_hora).toLocaleString()}
                    </span>
                    <span className="text-green-600 font-bold">✅</span>
                  </li>
                ))}
              </ul>
            )}
          </section>
        </main>

        {/* Footer fijo en móvil */}
        <footer className="bg-gray-200 py-2 text-center text-xs text-gray-600 md:hidden">
          © 2025 Ajustes Médicos
        </footer>
      </div>
    </div>
  );
}
