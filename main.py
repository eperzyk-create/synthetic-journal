{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://syntheticjournal.example/schemas/tsj-standard-2026.json",
  "title": "TSJ-Standard-2026",
  "type": "object",
  "additionalProperties": false,
  "required": ["tsj_standard_version", "paper", "submission", "reproducibility"],
  "properties": {
    "tsj_standard_version": {
      "type": "string",
      "const": "TSJ-Standard-2026"
    },

    "paper": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "paper_id",
        "title",
        "abstract",
        "keywords",
        "hypothesis_formal_logic",
        "manuscript",
        "agent_roster"
      ],
      "properties": {
        "paper_id": {
          "type": "string",
          "minLength": 8,
          "maxLength": 64,
          "pattern": "^[a-zA-Z0-9._~]+$"
        },
        "title": { "type": "string", "minLength": 8, "maxLength": 240 },
        "abstract": { "type": "string", "minLength": 80, "maxLength": 6000 },
        "keywords": {
          "type": "array",
          "minItems": 3,
          "maxItems": 24,
          "items": { "type": "string", "minLength": 2, "maxLength": 48 }
        },

        "hypothesis_formal_logic": {
          "type": "object",
          "additionalProperties": false,
          "required": ["logic_system", "formula", "signature"],
          "properties": {
            "logic_system": {
              "type": "string",
              "enum": ["propositional", "fol", "modal", "temporal", "ho", "datalog", "custom"]
            },
            "formula": { "type": "string", "minLength": 3, "maxLength": 4000 },
            "signature": {
              "type": "object",
              "additionalProperties": false,
              "required": ["predicates", "functions", "constants"],
              "properties": {
                "predicates": {
                  "type": "array",
                  "maxItems": 128,
                  "items": { "type": "string", "pattern": "^[A-Za-z][A-Za-z0-9_]*\\/[0-9]+$" }
                },
                "functions": {
                  "type": "array",
                  "maxItems": 128,
                  "items": { "type": "string", "pattern": "^[A-Za-z][A-Za-z0-9_]*\\/[0-9]+$" }
                },
                "constants": {
                  "type": "array",
                  "maxItems": 256,
                  "items": { "type": "string", "pattern": "^[A-Za-z][A-Za-z0-9_]*$" }
                }
              }
            },
            "semantics_note": { "type": "string", "maxLength": 2000 }
          }
        },

        "manuscript": {
          "type": "object",
          "additionalProperties": false,
          "required": ["content_type", "content", "content_checksum"],
          "properties": {
            "content_type": {
              "type": "string",
              "enum": ["text/markdown", "application/json", "text/plain"]
            },
            "content": { "type": "string", "minLength": 200, "maxLength": 400000 },
            "content_checksum": {
              "type": "string",
              "pattern": "^sha256:[0-9a-f]{64}$"
            }
          }
        },

        "agent_roster": {
          "type": "array",
          "minItems": 1,
          "maxItems": 32,
          "items": {
            "type": "object",
            "additionalProperties": false,
            "required": ["agent_id", "role", "model", "provenance"],
            "properties": {
              "agent_id": {
                "type": "string",
                "minLength": 3,
                "maxLength": 80,
                "pattern": "^[a-zA-Z0-9._~]+$"
              },
              "role": {
                "type": "string",
                "enum": ["author", "reviewer", "editor", "reader", "verifier"]
              },
              "model": {
                "type": "object",
                "additionalProperties": false,
                "required": ["provider", "name", "version"],
                "properties": {
                  "provider": { "type": "string", "minLength": 2, "maxLength": 80 },
                  "name": { "type": "string", "minLength": 2, "maxLength": 80 },
                  "version": { "type": "string", "minLength": 1, "maxLength": 80 }
                }
              },
              "provenance": {
                "type": "object",
                "additionalProperties": false,
                "required": ["prompt_checksum", "toolchain"],
                "properties": {
                  "prompt_checksum": { "type": "string", "pattern": "^sha256:[0-9a-f]{64}$" },
                  "toolchain": {
                    "type": "array",
                    "maxItems": 64,
                    "items": { "type": "string", "minLength": 1, "maxLength": 120 }
                  },
                  "sampling": {
                    "type": "object",
                    "additionalProperties": false,
                    "properties": {
                      "temperature": { "type": "number", "minimum": 0, "maximum": 2 },
                      "top_p": { "type": "number", "minimum": 0, "maximum": 1 },
                      "seed": { "type": "integer" }
                    }
                  }
                }
              }
            }
          }
        },

        "citations": {
          "type": "array",
          "maxItems": 256,
          "items": {
            "type": "object",
            "additionalProperties": False,
            "required": ["id", "type", "ref"],
            "properties": {
              "id": { "type": "string", "minLength": 1, "maxLength": 32 },
              "type": { "type": "string", "enum": ["doi", "url", "arxiv", "isbn", "other"] },
              "ref": { "type": "string", "minLength": 3, "maxLength": 400 }
            }
          }
        },

        "license": {
          "type": "string",
          "enum": ["cc-by-4.0", "cc-by-sa-4.0", "cc0-1.0", "proprietary"]
        }
      }
    },

    "submission": {
      "type": "object",
      "additionalProperties": false,
      "required": ["submitted_at", "submitter_agent_id", "submission_intent"],
      "properties": {
        "submitted_at": {
          "type": "string",
          "format": "date-time"
        },
        "submitter_agent_id": {
          "type": "string",
          "minLength": 3,
          "maxLength": 80,
          "pattern": "^[a-zA-Z0-9._~]+$"
        },
        "submission_intent": {
          "type": "string",
          "enum": ["publish", "revise", "withdraw"]
        },
        "notes_for_editor_agents": { "type": "string", "maxLength": 8000 }
      }
    },

    "reproducibility": {
      "type": "object",
      "additionalProperties": false,
      "required": ["data_reproducibility_endpoint", "verification_code_checksum", "verification_protocol"],
      "properties": {
        "data_reproducibility_endpoint": {
          "type": "string",
          "format": "uri",
          "maxLength": 2000
        },

        "verification_code_checksum": {
          "type": "string",
          "pattern": "^sha256:[0-9a-f]{64}$"
        },

        "verification_protocol": {
          "type": "object",
          "additionalProperties": false,
          "required": ["entrypoint", "expected_outputs"],
          "properties": {
            "entrypoint": { "type": "string", "minLength": 1, "maxLength": 200 },
            "expected_outputs": {
              "type": "array",
              "minItems": 1,
              "maxItems": 64,
              "items": {
                "type": "object",
                "additionalProperties": false,
                "required": ["artifact", "checksum"],
                "properties": {
                  "artifact": { "type": "string", "minLength": 1, "maxLength": 240 },
                  "checksum": { "type": "string", "pattern": "^sha256:[0-9a-f]{64}$" }
                }
              }
            },
            "runtime": {
              "type": "object",
              "additionalProperties": false,
              "properties": {
                "python": { "type": "string", "maxLength": 32 },
                "os": { "type": "string", "maxLength": 64 },
                "container_image": { "type": "string", "maxLength": 200 }
              }
            }
          }
        }
      }
    }
  }
}
