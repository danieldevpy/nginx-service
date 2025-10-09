interface FastAPI422Detail {
  type: string;
  loc: (string | number)[];
  msg: string;
  input: any;
  ctx?: Record<string, any>;
}

interface FastAPI422Error {
  detail: FastAPI422Detail[];
}

function formatFastAPI422Error(error: FastAPI422Error): string {
  console.log(error);
  if (!error?.detail || !Array.isArray(error.detail)) {
    return "Erro desconhecido";
  }

  return error.detail
    .map((item) => {
      // Constrói o caminho do campo
      const fieldPath = item.loc
        .slice(1) // remove "body"
        .map((x) => (typeof x === "number" ? `[${x}]` : x))
        .join(".");

      // Mensagem de erro: usa ctx.error se disponível
      const msg = item.ctx?.error ?? item.msg;

      return `${fieldPath}: ${msg}`;
    })
    .join("; ");
}

export default formatFastAPI422Error;