
import React, { Component } from 'react'
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import { withStyles } from '@material-ui/core';
import { getTerms } from '../services/TermService'

const styles = theme => ({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  formControl: {
    margin: theme.spacing.unit,
    minWidth: 120,
  },
  selectEmpty: {
    marginTop: theme.spacing.unit * 2,
  },
});


class MainPage extends Component {
  constructor(){
    super()
    this.state = {
      terms: [],
      selectedTerm: null
    }
    this.getTerms = this.getTerms.bind(this)
  }
  
  async getTerms(){
    try{
      const terms = await getTerms()
      console.log(terms)
      this.setState({
        terms
      })
    }catch(e){
      console.error(e)
      throw e
    }
  }

  componentDidMount(){
    this.getTerms()
  }
  render() {
    const {
      classes
    } = this.props

    const {
      terms
    } = this.state
    return(
      <FormControl className={classes.formControl}>
          <InputLabel htmlFor="age-simple">Term</InputLabel>
          <Select
            value={1}
            onChange={this.handleChange}
            inputProps={{
              name: 'age',
              id: 'age-simple',
            }}
          >
            <MenuItem value="">
              <em>Select a term</em>
            </MenuItem>
            { terms.map( term => (
              <MenuItem value={term.id}>term.term</MenuItem>
            ))}
          </Select>
        </FormControl>
    )

  }
}

export default withStyles(styles)(MainPage)