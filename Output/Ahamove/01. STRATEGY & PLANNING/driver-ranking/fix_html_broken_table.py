import re

with open("2026-05-driver-ranking-params.html", "r", encoding="utf-8") as f:
    content = f.read()

broken_str = '<td class="num" style="colo      <!-- CALIBRATION -->'

fixed_str = '''<td class="num" style="color:var(--blue);">240 × 1.1 = 264</td>
              <td><span style="font-family:'Montserrat',monospace;font-size:16px;font-weight:800;color:var(--blue);">264</span></td>
            </tr>
            <tr>
              <td><span class="rank-un">L6</span> <span class="layer-badge l6" style="margin-left:4px;">L6</span></td>
              <td class="num">~55k/h · 220k/ca</td>
              <td class="num">220</td>
              <td class="num" style="color:var(--text-sec);">220 × 1.0 = 220</td>
              <td><span style="font-family:'Montserrat',monospace;font-size:16px;font-weight:800;color:var(--text-sec);">220</span></td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- CALIBRATION -->'''

if broken_str in content:
    content = content.replace(broken_str, fixed_str)
    with open("2026-05-driver-ranking-params.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("Fixed broken table!")
else:
    print("Broken string not found!")

