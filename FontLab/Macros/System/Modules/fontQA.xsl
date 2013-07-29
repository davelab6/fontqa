<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

	<xsl:template match="/">
		<HTML>
			<HEAD>
				<script language="JavaScript">
				myHelp = null;
				
				function cbInfo_onclick()
				{display_row(document.FORM1.cbInfo, "class_I");}

				function cbPass_onclick()
				{display_row(document.FORM1.cbPass, "class_P");}

				function cbWarn_onclick()
				{display_row(document.FORM1.cbWarn, "class_W");}

				function cbErr_onclick()
				{display_row(document.FORM1.cbErr, "class_E");}

				function display_table(table_id)
				{table_id.style.display = (table_id.style.display == "none" ) ? "" : "none";}

				function display_row(cb_id, row_classname)
				{
					rowColl = document.all.tags("TR");
					for (i=0; i!=rowColl.length; i++) {
						if (rowColl(i).className == row_classname)
						{
							if (cb_id.checked)
							{
								rowColl(i).style.display = "";
							}
							else
							{
								rowColl(i).style.display = "none";
							}
						}
					}
				}
				
				function showHelp(id) 
				{
					if (myHelp != null){hideHelp();}
					myHelp = document.getElementById(id);
					myHelp.style.display = "block";
				}
				
				function hideHelp() 
				{
				myHelp.style.display = "none";
				}
				</script>
				<STYLE>
					BODY			 {font-family      : Trebuchet MS}
					H1				 {font-size				 : 150%;
											font-weight      : bold;
											color            : #003333;
											background-color : #E6F2F2}
					H2				 {font-size        : 110%;
											font-weight      : bold;
											color            : #003333;
											background-color : #E7E9ED}
					TABLE			 {font-family      : Trebuchet MS;
											width            : 100%}
					TABLE.detail {display        : none}
					TR				 {background-color : #E6F2F2; color : #003333}
					TR.title,
					TR.caption {background-color : #CFE5E5; font-weight : bold}
					.class_A	 {background-color : #000000; color : #ffff00}
					.class_E	 {background-color : #ffB2CC}
					.class_W	 {background-color : #FFF2B2}
					.class_P	 {background-color : #B2ffD9}
					.class_I	 {background-color : #B2CCFF}
					TR.class_N {background-color : #F7F9FD}
					TD				 {padding-left		 : 4;
											font-size        : 75%}
					DIV.help	 {position         : absolute;
											display          : none;
											cursor           : pointer;
											border-width     : 1px;
											border-style     : solid;
											border-color     : #182949;
											padding          : 2px;
											color            : #182949;
											background-color : #E7E9ED;}
				</STYLE>
				<TITLE>FontQA Report</TITLE>
			</HEAD>
			<BODY>
				<FORM NAME="FORM1">
				<H1>FontQA Report</H1>
				<TABLE><TR>
					<TD BGCOLOR="#ffffff" WIDTH="20%">Show</TD>
					<TD CLASS="class_I" WIDTH="20%">
					<xsl:text disable-output-escaping="yes">&lt;INPUT</xsl:text>
					id='cbInfo' type='checkbox' name='cbInfo' onclick='cbInfo_onclick()'
					<xsl:text disable-output-escaping="yes">checked&gt;</xsl:text>
					Info
					</TD>
					<TD CLASS="class_P" WIDTH="20%">
					<xsl:text disable-output-escaping="yes">&lt;INPUT</xsl:text>
					id='cbPass' type='checkbox' name='cbPass' onclick='cbPass_onclick()'
					<xsl:text disable-output-escaping="yes">checked &gt;</xsl:text>
					Pass
					</TD>
					<TD CLASS="class_W" WIDTH="20%">
					<xsl:text disable-output-escaping="yes">&lt;INPUT</xsl:text>
					id='cbWarn' type='checkbox' name='cbWarn' onclick='cbWarn_onclick()'
					<xsl:text disable-output-escaping="yes">checked &gt;</xsl:text>
					Warning
					</TD>
					<TD CLASS="class_E" WIDTH="20%">
					<xsl:text disable-output-escaping="yes">&lt;INPUT</xsl:text>
					id='cbErr' type='checkbox' name='cbErr' onclick='cbErr_onclick()'
					<xsl:text disable-output-escaping="yes">checked &gt;</xsl:text>
					Error
					</TD>
				</TR></TABLE>
				<TABLE>
					<TR>
						<TD WIDTH="20%"><I>Run DateTime: </I></TD>
						<TD><xsl:value-of select="fontQA/@RunDateTime"/></TD>
					</TR>
				</TABLE>
				<BR/>
				<xsl:apply-templates select="fontQA/FontList"/>
				<BR/>
				<xsl:apply-templates select="fontQA/TestSuite"/>
			</FORM>
			</BODY>
		</HTML>
	</xsl:template>

	<xsl:template match="FontList">
		<TABLE>
			<TR CLASS="title"><TD COLSPAN="2">Font List</TD></TR>
			<TR CLASS="caption">
				<TD WIDTH="20%">FullName</TD>
				<TD WIDTH="80%">Path</TD>
			</TR>
			<xsl:for-each select="Font">
				<TR class="class_I"><xsl:apply-templates select="."/></TR>
			</xsl:for-each>
			<TR>
				<TD><B>Total</B></TD>
				<TD><B><xsl:value-of select="count(Font)"/></B></TD>
			</TR>
		</TABLE>
	</xsl:template>

	<xsl:template match="Font">
		<TD><xsl:value-of select="@FullName"/></TD>
		<TD><xsl:value-of select="@Path"/></TD>
	</xsl:template>

	<xsl:template match="TestSuite">
		<TABLE>
			<TR CLASS="title"><TD COLSPAN="7">Test Suite</TD></TR>
			<TR CLASS="caption">
				<TD WIDTH="20%">Test Block</TD>
				<TD WIDTH="10%">Total</TD>
				<TD WIDTH="14%">Info</TD>
				<TD WIDTH="14%">Pass</TD>
				<TD WIDTH="14%">Warning</TD>
				<TD WIDTH="14%">Error</TD>
				<TD WIDTH="14%">Abort</TD>
			</TR>
			<xsl:for-each select="TestBlock">
				<TR>
					<TD>
						<xsl:text disable-output-escaping="yes">&lt;INPUT</xsl:text>
						id='cb_<xsl:value-of select="@tag"/>' type='checkbox' name='cb_<xsl:value-of select="@tag"/>' onclick='display_table(table_<xsl:value-of select="@tag"/>)'
						<xsl:text disable-output-escaping="yes">checked &gt;</xsl:text>
						<xsl:text disable-output-escaping="yes">&lt;A</xsl:text>
						HREF='#<xsl:value-of select="@tag"/>'
						<xsl:text disable-output-escaping="yes">&gt;</xsl:text>
						<xsl:value-of select="@name"/>
						<xsl:text disable-output-escaping="yes">&lt;/A&gt;</xsl:text>
					</TD>
					<TD><B><xsl:value-of select="count(TestItem)"/></B></TD>
					<TD>
						<xsl:if test="count(TestItem[@ErrorType='I']) > 0">
							<xsl:attribute name="CLASS">class_I</xsl:attribute>
						</xsl:if>
						<xsl:value-of select="count(TestItem[@ErrorType='I'])"/></TD>
					<TD>
						<xsl:if test="count(TestItem[@ErrorType='P']) > 0">
							<xsl:attribute name="CLASS">class_P</xsl:attribute>
						</xsl:if>
						<xsl:value-of select="count(TestItem[@ErrorType='P'])"/>
					</TD>
					<TD>
						<xsl:if test="count(TestItem[@ErrorType='W']) > 0">
							<xsl:attribute name="CLASS">class_W</xsl:attribute>
						</xsl:if>
						<xsl:value-of select="count(TestItem[@ErrorType='W'])"/>
					</TD>
					<TD>
						<xsl:if test="count(TestItem[@ErrorType='E']) > 0">
							<xsl:attribute name="CLASS">class_E</xsl:attribute>
						</xsl:if>
						<xsl:value-of select="count(TestItem[@ErrorType='E'])"/>
					</TD>
					<TD>
						<xsl:if test="count(TestItem[@ErrorType='A']) > 0">
							<xsl:attribute name="CLASS">class_A</xsl:attribute>
						</xsl:if>
						<xsl:value-of select="count(TestItem[@ErrorType='A'])"/>
					</TD>
				</TR>
			</xsl:for-each>
			<TR CLASS="caption">
				<TD>Total</TD>
				<TD><xsl:value-of select="count(TestBlock/TestItem)"/></TD>
				<TD><xsl:value-of select="count(TestBlock/TestItem[@ErrorType='I'])"/></TD>
				<TD><xsl:value-of select="count(TestBlock/TestItem[@ErrorType='P'])"/></TD>
				<TD><xsl:value-of select="count(TestBlock/TestItem[@ErrorType='W'])"/></TD>
				<TD><xsl:value-of select="count(TestBlock/TestItem[@ErrorType='E'])"/></TD>
				<TD><xsl:value-of select="count(TestBlock/TestItem[@ErrorType='A'])"/></TD>
			</TR>
		</TABLE>
		<HR/>
		<xsl:for-each select="TestBlock">
			<xsl:apply-templates select="."/>
		</xsl:for-each>
	</xsl:template>

	<xsl:template match="TestBlock">
		<xsl:text disable-output-escaping="yes">&lt;TABLE</xsl:text>
		id='table_<xsl:value-of select="@tag"/>'
		<xsl:text disable-output-escaping="yes">&gt;</xsl:text>
			<TR CLASS="title"><TD COLSPAN="3">
				<xsl:text disable-output-escaping="yes">&lt;A</xsl:text>
				NAME='<xsl:value-of select="@tag"/>'
				<xsl:text disable-output-escaping="yes">&gt;</xsl:text>
				<xsl:value-of select="@name"/>
				<xsl:text disable-output-escaping="yes">&lt;/A&gt;</xsl:text>
			</TD></TR>
			<TR CLASS="caption">
				<TD WIDTH="20%">Test</TD>
				<TD WIDTH="40%">Message</TD>
				<TD WIDTH="40%">Details</TD>
			</TR>
			<xsl:for-each select="TestItem">
				<xsl:apply-templates select="."/>
			</xsl:for-each>
		<xsl:text disable-output-escaping="yes">&lt;/TABLE&gt;</xsl:text>
		<BR/>
	</xsl:template>

	<xsl:template match="TestItem">
		<xsl:text disable-output-escaping="yes">&lt;TR</xsl:text>
		class='class_<xsl:value-of select="@ErrorType"/>'
		<xsl:text disable-output-escaping="yes">&gt;</xsl:text>
		<TD VALIGN="TOP">
			<xsl:text disable-output-escaping="yes">&lt;INPUT</xsl:text>
			style='width:16px; height:16px; margin-right:8px; cursor:s-resize' type='button' onclick='display_table(table_<xsl:value-of select="parent::node()/@tag"/>_<xsl:value-of select="@tag"/>)'
			<xsl:text disable-output-escaping="yes"> &gt;</xsl:text>
			<xsl:choose>
				<xsl:when test="count(Description) = 1">
					<DIV CLASS="help" onClick="hideHelp()">
						<xsl:attribute name="id">help_<xsl:value-of select="parent::node()/@tag"/>_<xsl:value-of select="@tag"/></xsl:attribute>
						<TABLE style="width:85%">
							<TR CLASS="title"><TD>Help: <xsl:value-of select="@name"/></TD></TR>
							<TR><TD><xsl:value-of select="Description"/></TD></TR>
						</TABLE>
					</DIV>
					<A style="cursor:help">
						<xsl:attribute name="onClick">
							showHelp('help_<xsl:value-of select="parent::node()/@tag"/>_<xsl:value-of select="@tag"/>')
						</xsl:attribute>
						<xsl:value-of select="@name"/>
					</A>
				</xsl:when>
				<xsl:otherwise><xsl:value-of select="@name"/></xsl:otherwise>
			</xsl:choose>
		</TD>
		<TD VALIGN="TOP"> <xsl:value-of select="@Message"/> </TD>
		<TD VALIGN="TOP"> <xsl:value-of select="@Details"/> </TD>
		<xsl:text disable-output-escaping="yes">&lt;/TR&gt;</xsl:text>
		<xsl:text disable-output-escaping="yes">&lt;TR</xsl:text>
		class='class_<xsl:value-of select="@ErrorType"/>'
		<xsl:text disable-output-escaping="yes">&gt;</xsl:text>
		<TD colspan="3">
		<xsl:text disable-output-escaping="yes">&lt;TABLE</xsl:text>
		STYLE='{display:none}' id='table_<xsl:value-of select="parent::node()/@tag"/>_<xsl:value-of select="@tag"/>'
		<xsl:text disable-output-escaping="yes">&gt;</xsl:text>
		<xsl:for-each select="TestDetail">
			<xsl:apply-templates select="."/>
		</xsl:for-each>
		<xsl:text disable-output-escaping="yes">&lt;/TABLE&gt;</xsl:text>
		</TD>
		<xsl:text disable-output-escaping="yes">&lt;/TR&gt;</xsl:text>
	</xsl:template>

	<xsl:template match="TestDetail">
		<xsl:text disable-output-escaping="yes">&lt;TR</xsl:text>
		class='class_<xsl:value-of select="@ErrorType"/>'
		<xsl:text disable-output-escaping="yes">&gt;</xsl:text>
			<TD WIDTH="20%" VALIGN="TOP"> <xsl:value-of select="@FontName"/> </TD>
			<TD WIDTH="40%" VALIGN="TOP"> <xsl:value-of select="@Message"/> </TD>
			<TD WIDTH="40%" VALIGN="TOP"> <xsl:value-of select="@Details"/> </TD>
		<xsl:text disable-output-escaping="yes">&lt;/TR&gt;</xsl:text>
	</xsl:template>

</xsl:stylesheet>
