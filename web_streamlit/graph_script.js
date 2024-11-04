const selectedNodes = [];

network.on('selectNode', function (params) {
    updateNodeInfo(params.nodes);
});

network.on('deselectNode', function (params) {
    updateNodeInfo(params.nodes);
});

network.on('selectEdge', function (params) {
    updateEdgeInfo(params.edges);
});

network.on('deselectEdge', function (params) {
    updateEdgeInfo(params.edges);
});
function updateNodeInfo(_selectedNodes) {

    selectedNodes.length = 0;
    _selectedNodes.forEach(nodeId => {
            selectedNodes.push(nodeId)
//        const node = network.body.data.nodes.get(nodeId);
//
//        let incomingEdges = [];
//        let outgoingEdges = [];
//
//        allEdges.forEach(edge => {
//            if (edge.to === nodeId) {
//                incomingEdges.push(edge);
//            } else if (edge.from === nodeId) {
//                outgoingEdges.push(edge);
//            }
//        });
//
//        node_info_html += `<br><strong>Node:</strong> ${node.label || node.id}<br>`;
//
//        node_info_html += '<strong>Incoming Edges:</strong><ul>';
//        incomingEdges.forEach(edge => {
//            node_info_html += `<li>From: ${edge.from}, Label: ${edge.label || 'N/A'}</li>`;
//        });
//        node_info_html += '</ul>';
//
//        node_info_html += '<strong>Outgoing Edges:</strong><ul>';
//        outgoingEdges.forEach(edge => {
//            node_info_html += `<li>To: ${edge.to}, Label: ${edge.label || 'N/A'}</li>`;
//        });
//        node_info_html += '</ul>';
    });
//
//    var node_info_placeholder = window.parent.document.getElementById('node_info_placeholder');
//    node_info_placeholder.innerHTML = node_info_html;
}

function updateEdgeInfo(selectedEdges) {
    let node_info_html = '<strong>Selected Nodes:</strong><br>';
    selectedNodes.forEach(nodeId => {
        const node = network.body.data.nodes.get(nodeId);
        let incomingEdges = [];
        let outgoingEdges = [];
        let allEdges = network.getConnectedEdges(nodeId);
        allEdges.forEach(edge => {
            if (edge.to === nodeId) {
                incomingEdges.push(edge);
            } else if (edge.from === nodeId) {
                outgoingEdges.push(edge);
            }
        });

        node_info_html += `<br><strong>Node:</strong> ${node.label || node.id}<br>`;

        node_info_html += '<strong>Incoming Edges:</strong><ul>';
        incomingEdges.forEach(edge => {
            node_info_html += `<li>From: ${edge.from}, Label: ${edge.label || 'N/A'}</li>`;
        });
        node_info_html += '</ul>';

        node_info_html += '<strong>Outgoing Edges:</strong><ul>';
        outgoingEdges.forEach(edge => {
            node_info_html += `<li>To: ${edge.to}, Label: ${edge.label || 'N/A'}</li>`;
        });
        node_info_html += '</ul>';
    });
    var node_info_placeholder = window.parent.document.getElementById('node_info_placeholder');
    node_info_placeholder.innerHTML = node_info_html;
    let edge_info_html = '<strong>Selected Edges:</strong><br>';

    selectedEdges.forEach(edgeId => {
        const edge = network.body.data.edges.get(edgeId);
        edge_info_html += `<br>From: ${edge.from}, To: ${edge.to}, Label: ${edge.label || 'N/A'}`;
    });

    node_info_placeholder.innerHTML += edge_info_html;
}