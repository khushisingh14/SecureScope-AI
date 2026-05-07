import { Component } from "react";

export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { error: null };
  }

  static getDerivedStateFromError(error) {
    return { error };
  }

  componentDidCatch(error, info) {
    console.error("UI render failure", error, info);
  }

  render() {
    if (this.state.error) {
      return (
        <div className="glass rounded-lg p-5">
          <p className="font-bold text-white">Something went wrong</p>
          <p className="mt-2 text-sm text-slate-400">The view recovered from a rendering error. Refresh the page or try the action again.</p>
          <button
            onClick={() => this.setState({ error: null })}
            className="mt-4 rounded-lg border border-cyan/30 px-3 py-2 text-sm font-semibold text-cyan hover:bg-cyan/10"
          >
            Retry
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
