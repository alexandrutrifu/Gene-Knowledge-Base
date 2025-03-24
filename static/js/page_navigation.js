const navEntry = performance.getEntriesByType("navigation")[0];

if (
  navEntry?.type === "reload" &&
  window.location.pathname.startsWith("/gene/")
) {
  window.location.replace("/");
}