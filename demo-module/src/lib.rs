wit_bindgen::generate!("demo");

use demo_types::{ResultType, RuntimeValue};

struct Exports;
impl crate::wit::Wit for Exports {
    fn something() -> crate::wit::ResultType {
        ResultType {
            value: RuntimeValue::String("Rust demo response...".to_string()),
        }
    }
}

export_demo!(Exports);
