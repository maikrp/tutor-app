import { useEffect, useState } from "react";
import { supabase } from "./supabase";

export default function App() {
  const [pendientes, setPendientes] = useState([]);
  const [realizados, setRealizados] = useState([]);
  const [paciente, setPaciente] = useState(null);
  const [hayManana, setHayManana] = useState(false);
  const [filtroTipo, setFiltroTipo] = useState("todos");

  useEffect(() => {
    fetchPaciente();
    fetchAjustes();
  }, [filtroTipo]);

  // === Cargar paciente ===
  async function fetchPaciente() {
    const { data, error } = await supabase
      .from("pacientes")
      .select("*")
      .order("created_at", { ascending: false })
      .limit(1);

    if (!error && data && data.length > 0) {
      setPaciente(data[0]);
    }
  }

  // === Cargar ajustes filtrados por fecha actual ===
  async function fetchAjustes() {
    const hoy = new Date();
    const yyyy = hoy.getFullYear();
    const mm = String(hoy.getMonth() + 1).padStart(2, "0");
    const dd = String(hoy.getDate()).padStart(2, "0");
    const hoyISO = `${yyyy}-${mm}-${dd}`;

    const manana = new Date(hoy);
    manana.setDate(hoy.getDate() + 1);
    const yyyy2 = manana.getFullYear();
    const mm2 = String(manana.getMonth() + 1).padStart(2, "0");
    const dd2 = String(manana.getDate()).padStart(2, "0");
    const mananaISO = `${yyyy2}-${mm2}-${dd2}`;

    let queryPend = supabase
      .from("ajustes")
      .select("*")
      .eq("realizado", false)
      .gte("fecha_hora", `${hoyISO}T00:00:00`)
      .lt("fecha_hora", `${hoyISO}T23:59:59`)
      .order("fecha_hora", { ascending: true });

    let queryReal = supabase
      .from("ajustes")
      .select("*")
      .eq("realizado", true)
      .gte("fecha_hora", `${hoyISO}T00:00:00`)
      .lt("fecha_hora", `${hoyISO}T23:59:59`)
      .order("fecha_hora", { ascending: true });

    if (filtroTipo !== "todos") {
      queryPend = queryPend.eq("metodo", filtroTipo);
      queryReal = queryReal.eq("metodo", filtroTipo);
    }

    const { data: pend } = await queryPend;
    const { data: real } = await queryReal;
    setPendientes(pend || []);
    setRealizados(real || []);

    // === Verificar si hay ajustes mañana ===
    const { data: ajustesManana } = await supabase
      .from("ajustes")
      .select("id")
      .gte("fecha_hora", `${mananaISO}T00:00:00`)
      .lt("fecha_hora", `${mananaISO}T23:59:59`);

    setHayManana(ajustesManana && ajustesManana.length > 0);
  }

  async function marcarRealizado(id) {
    await supabase.from("ajustes").update({ realizado: true }).eq("id", id);
    fetchAjustes();
  }

  function tituloFiltro() {
    if (filtroTipo === "todos") return "Todos";
    if (filtroTipo === "Clicks") return "Clicks";
    if (filtroTipo === "Length") return "Length";
  }

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="w-full max-w-sm bg-white rounded-3xl shadow-2xl flex flex-col overflow-hidden border border-gray-200">
        
        {/* Header institucional */}
        <header className="bg-blue-900 text-white py-4 shadow px-4">
          <h1 className="text-base font-bold text-center">Control de Ajustes</h1>
          <span className="text-xs italic block text-center">
            ({tituloFiltro()})
          </span>

          {/* Datos del paciente */}
          {paciente && (
            <div className="text-xs mt-2 bg-blue-800 p-2 rounded-lg">
              <p><b>Paciente:</b> {paciente.patient_id}</p>
              <p><b>Case ID:</b> {paciente.case_id}</p>
              <p><b>Descripción:</b> {paciente.case_description}</p>
              <p><b>Hueso:</b> {paciente.bone_type}</p>
              <p><b>Lado:</b> {paciente.side}</p>
            </div>
          )}

          {/* Contadores */}
          <div className="text-[11px] mt-2 flex justify-between">
            <span>⏳ Pendientes: {pendientes.length}</span>
            <span>✅ Confirmados: {realizados.length}</span>
          </div>

          {/* Aviso ajustes mañana */}
          {hayManana && (
            <p className="mt-1 text-yellow-400 text-xs text-center font-semibold">
              ⚠️ Hay ajustes programados para mañana
            </p>
          )}
        </header>

        {/* Selector de filtro */}
        <div className="bg-gray-50 flex justify-around py-3 border-b">
          {["todos", "Clicks", "Length"].map((tipo) => (
            <button
              key={tipo}
              onClick={() => setFiltroTipo(tipo)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition ${
                filtroTipo === tipo
                  ? "bg-blue-700 text-white shadow-md"
                  : "bg-white text-gray-700 border"
              }`}
            >
              {tipo}
            </button>
          ))}
        </div>

        {/* Contenido */}
        <main className="flex-1 overflow-y-auto p-4 space-y-6">
          {/* Pendientes */}
          <section>
            <h2 className="text-base font-semibold text-gray-700 mb-3">Pendientes de Hoy</h2>
            {pendientes.length === 0 ? (
              <p className="text-gray-400 text-center text-sm">✅ No hay ajustes pendientes</p>
            ) : (
              <div className="space-y-4">
                {pendientes.map((a) => (
                  <div
                    key={a.id}
                    className="p-4 rounded-2xl border border-gray-100 shadow-sm bg-white"
                  >
                    <p className="font-semibold text-gray-800 text-sm">
                      {new Date(a.fecha_hora).toLocaleString()}
                    </p>
                    <p className="text-xs text-gray-500 italic">Método: {a.metodo}</p>
                    <p className="mt-2 text-gray-600 text-sm">
                      🔴 {a.red} | 🟠 {a.orange} | 🟡 {a.yellow} | 🟢 {a.green} | 🔵 {a.blue} | 🟣 {a.purple}
                    </p>
                    <button
                      onClick={() => marcarRealizado(a.id)}
                      className="mt-3 w-full py-2 rounded-xl bg-gradient-to-r from-green-600 to-blue-600 text-white font-semibold shadow hover:opacity-90 transition"
                    >
                      Confirmar realizado
                    </button>
                  </div>
                ))}
              </div>
            )}
          </section>

          {/* Historial */}
          <section>
            <h2 className="text-base font-semibold text-gray-700 mb-3">Historial de Hoy</h2>
            {realizados.length === 0 ? (
              <p className="text-gray-400 text-center text-sm">No hay ajustes confirmados aún</p>
            ) : (
              <ul className="space-y-2">
                {realizados.map((a) => (
                  <li
                    key={a.id}
                    className="p-3 rounded-xl border border-gray-100 flex items-center justify-between shadow-sm bg-white"
                  >
                    <div>
                      <span className="text-gray-800 text-sm block">
                        {new Date(a.fecha_hora).toLocaleString()}
                      </span>
                      <span className="text-xs text-gray-500 italic">Método: {a.metodo}</span>
                    </div>
                    <span className="text-green-600 font-bold text-lg">✅</span>
                  </li>
                ))}
              </ul>
            )}
          </section>
        </main>
      </div>
    </div>
  );
}
