"""Eugenia AGI — Main entry point for python -m nucleus."""
from nucleus.nucleus_knowledge_system import demo, KnowledgeSystem


def main():
    """Run Eugenia AGI system."""
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "demo":
            demo()
        elif sys.argv[1] == "query" and len(sys.argv) > 2:
            system = KnowledgeSystem()
            result = system.query(" ".join(sys.argv[2:]))
            print(f"AGI Result: {result}")
        else:
            print("Usage: python -m nucleus [demo|query <text>]")
    else:
        demo()


if __name__ == "__main__":
    main()
