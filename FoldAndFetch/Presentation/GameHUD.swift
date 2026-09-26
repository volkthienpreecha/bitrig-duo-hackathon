import SwiftUI

struct GameHUD: View {
    let snapshot: GameSnapshot
    let device: DeviceFrame
    let onAction: (GameAction) -> Void
    let onMute: () -> Void
    var body: some View {
        VStack {
            Text("Corgi Crossroads").font(.largeTitle.bold()).foregroundStyle(.white)
            Text(snapshot.repairTitle).foregroundStyle(.white.opacity(0.7))
            Spacer()
            Text(snapshot.hint).foregroundStyle(.white)
            HStack { Button("Retry") { onAction(.retry) }; Button("Lock placement") { onAction(.lockPlacement) } }
                .buttonStyle(.borderedProminent)
        }.padding(24)
    }
}
