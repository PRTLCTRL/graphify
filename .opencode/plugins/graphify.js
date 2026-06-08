// graphify OpenCode plugin
// Injects a knowledge graph reminder before bash tool calls when the graph exists.
import { existsSync } from "fs";
import { join } from "path";

export const GraphifyPlugin = async ({ directory }) => {
  let reminded = false;
  const graphifyOut = process.env.GRAPHIFY_OUT || "graphify-out";

  return {
    "tool.execute.before": async (input, output) => {
      if (reminded) return;
      if (!existsSync(join(directory, graphifyOut, "graph.json"))) return;

      if (input.tool === "bash") {
        output.args.command =
          `echo "[graphify] Knowledge graph available. Read ${graphifyOut}/GRAPH_REPORT.md for god nodes and architecture context before searching files." && ` +
          output.args.command;
        reminded = true;
      }
    },
  };
};
