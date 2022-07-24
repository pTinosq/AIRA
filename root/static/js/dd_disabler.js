function toggle_disable(element, disabled) {
    if (disabled) {
        element.disabled = true;
        document.getElementById(element.id + '_master').style.display = "none";
    } else {
        element.disabled = false;
        document.getElementById(element.id + '_master').style.display = "block";
    }
}

function handle_disabling(dropdown_options) {
    const aggregate_models = ['ContinuousModularModel'];
    const influence_models = ['ContinuousModularModel'];
    const conservative_influences = ['LinearInfluence', 'QuadraticMaximumInfluence'];
    const aggr_dd = document.getElementById("aggr_aside_dd");
    const inf_dd = document.getElementById("inf_aside_dd");
    const inf_fl = document.getElementById("inf_aside_fl");

    if (!aggregate_models.includes(dropdown_options["model_aside_dd"])) {
        toggle_disable(aggr_dd, true);
    } else {
        toggle_disable(aggr_dd, false);
    }

    if (!influence_models.includes(dropdown_options["model_aside_dd"])) {
        toggle_disable(inf_dd, true);
    } else {
        toggle_disable(inf_dd, false);
    }

    if (!conservative_influences.includes(dropdown_options["inf_aside_dd"]) || inf_dd.disabled == true) {
        toggle_disable(inf_fl, true);
    } else {
        toggle_disable(inf_fl, false);
    }
}

document.addEventListener("DOMContentLoaded", (event) => {
    // Aggregate, influence and influence conservativeness are only enabled on certain models
    // This event adds listeners to all the dropdowns (dd) and also does checks on load
    let dropdown_options = {
        "model_aside_dd": "",
        "inf_aside_dd": ""
    };

    for (const id in dropdown_options) {
        document.getElementById(id).onchange = function () {
            dropdown_options[id] = document.getElementById(id).value;
            handle_disabling(dropdown_options);
        }
        dropdown_options[id] = document.getElementById(id).value;
    }

    handle_disabling(dropdown_options);
})